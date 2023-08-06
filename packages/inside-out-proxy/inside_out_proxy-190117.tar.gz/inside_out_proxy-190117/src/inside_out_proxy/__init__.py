#!/usr/bin/env python
from __future__ import print_function, absolute_import

"""
'Inside Out' HTTP CNR Proxy


USAGE: See --helpfull


---

DETAILS: https://axc2.axiros.com/maxmd/HTTPCNRProxy

Opens http long polling connections to http(s) servers (given on CLI) and starts
receiving CNR jobs, which it processes, grouped by cpeids, concurrently.

In small intervals we post results back to the servers, syncronously.

"""

__author__ = 'Gunther Klessinger, Axiros GmbH, Germany'
__date__ = '2019-01-14'

from .version import version

# ... and greenlets for async/concurrency
from gevent import monkey

monkey.patch_all()

import os, json, sys, time, traceback

# We use ReactiveX for orchestration...
import rx

# flags:
from absl import app, flags

# Simple logging to stdout:
import requests, structlog, attr
from requests.auth import HTTPDigestAuth as digest
from requests.auth import HTTPBasicAuth as basic_auth
from threading import current_thread

from inside_out_proxy import axlog

log = None
tn = lambda: current_thread().name

FLAGS = flags.FLAGS
flags.DEFINE_string('user', 'testuser', 'Job server account name')
flags.DEFINE_string('password', 'testpassword', 'Job server account password')
flags.DEFINE_string('jobserver', 'http://127.0.0.1:8089', 'Job Server URL')
flags.DEFINE_integer('cnr_timeout', 2, 'Timeout for CNR Jobs')
flags.DEFINE_integer(
    'buffer_time', 2, 'Send results back within this time intervals (secs)'
)
flags.DEFINE_boolean('debug', False, 'Debug mode (extended logging)')

server = lambda: FLAGS.jobserver
now = lambda: time.time()
GS = rx.concurrency.GEventScheduler()
concurrent = lambda stream: stream.subscribe_on(GS)


pass_ = lambda ev: 0


def err(exc):
    f = traceback.format_exc()
    log.exception('Stream Exception', exc=str(exc), tb=f)
    return exc


stats, total_stats = {}, {}


def incr(key, stats=stats):
    stats[key] = stats.get(key, 0) + 1


def stats_clear():
    """run every stats post interval"""
    for k in stats:
        stats[k] = 0
    stats['cleared'] = now()


def stats_add_to_total():
    for k in stats:
        total_stats[k] = total_stats.get(k, 0) + stats.get(k, 0)


class ActiveCPEs:
    """namespace only
    this is fed from either a pubsub on SB Tier or only from local process, when
    standalone:
    """

    flags.DEFINE_integer(
        'active_cpe_expire',
        100,
        'If older than this (secs) then discard a cpe marked active. Something went wrong',
    )
    activate_s = rx.subjects.Subject()
    deactivate_s = rx.subjects.Subject()
    # current active ones:
    active_cpes = {}

    def add_active(ac, job):
        """
        called at job receival from poll or, when distributed from listeners
        returns None if cpe already active
        """
        cpeid = job.get('cpeid')
        if cpeid in ac.active_cpes:
            incr('already_active')
            log.info('Already active', cpeid=cpeid)
            return
        log.debug('Marking cpe active', cpeid=cpeid)
        ac.activate_s.on_next(cpeid)
        return job

    def active_cpes_maintainance(ac):
        log.info('Starting active cpes maint.')
        expire = FLAGS.active_cpe_expire

        def add(cpeid):
            have = ac.active_cpes.get(cpeid)
            if have is None or now() - have > expire:
                ac.active_cpes[cpeid] = now()

        def remove(cpeid):
            ac.active_cpes.pop(cpeid, None)
            return cpeid

        def purge_expired(ev):
            """only a cleanup to have our active_cpes not contain outdated ones
            """
            n = now()
            acs = ac.active_cpes
            for id in list(ac.active_cpes):
                ts = acs.get(id)
                if n - ts > expire:
                    log.warn('Expiring old cpe', cpeid=id)
                    acs.pop(id, None)

        ac.activate_s.map(add).subscribe_on(GS).subscribe(pass_, err)
        ac.deactivate_s.map(remove).subscribe_on(GS).subscribe(pass_, err)
        rx.Observable.interval(expire).map(purge_expired).subscribe(pass_, err)


active_cpes = ActiveCPEs()


@flags.validator('jobserver', message='Must be http server. No "/" at end')
def check_url(u):
    s = u.startswith
    return (s('http://') or s('https://')) and not u.endswith('/')


def dt(since):
    """time delta in millis"""
    return int((now() - since) * 1000)


def send_cnr(cnr):
    log.debug('CNR', **cnr)
    t0 = time.time()
    res = {'cpeid': cnr['cpeid']}
    try:
        url = cnr['url']
        if url.startswith('SELF'):
            url = url.replace('SELF', server() + '/fake_cnr')
            digest = basic_auth

        req = requests.get(
            url,
            auth=digest(cnr.get('user', ''), cnr.get('password', '')),
            timeout=cnr.get('timeout', FLAGS.cnr_timeout),
        )
        res['status'] = req.status_code

    except requests.exceptions.Timeout:
        res['status'] = 504
    except Exception as ex:
        res['status'] = 599
        res['details'] = str(ex)
    active_cpes.deactivate_s.on_next(cnr['cpeid'])
    res['pt'] = dt(t0)
    log.debug('CNR Result', **res)
    incr(res['status'])
    return res


def send_results(batch):
    """s is a batch of results from within buffer_time """
    if not batch:
        s = {'ts': now()}
    else:
        stats['active_count'] = len(active_cpes.active_cpes)
        stats['dt'] = dt(stats['cleared'])
        stats_add_to_total()
        s = {
            'ts': now(),
            'jobs': batch,
            'stats': {'int': stats, 'total': total_stats},
        }
    m = {}
    if FLAGS.debug:
        m = {'results': s}

    log.info('Sending results', **m) if batch else log.debug('Heartbeat')

    try:
        url = server() + '/results'
        res = requests.post(url, data=json.dumps(s), auth=server_auth)
        assert res.status_code < 300, 'Status code is %s' % res.status_code
    except Exception as ex:
        log.error('Could not send back result', ex=ex)
    stats_clear()


server_auth = None


def setup():
    global log, server_auth
    if FLAGS.debug:
        FLAGS.log_level = 10
    axlog.setup_logging()
    log = axlog.get_logger('inside_out_proxy')
    stats_clear()
    server_auth = basic_auth(FLAGS.user, FLAGS.password)


def main(argv):
    setup()

    def jobs(obs):
        url = server() + '/poll'
        while True:
            # FIXME sending all the time? What if tail -f ? is the job ?
            try:
                log.info('Connecting to job server', url=url)
                job = requests.get(url, stream=True, auth=server_auth)
                if job.status_code == 401:
                    log.exception('Unauthorized', user=FLAGS.user)
                    time.sleep(10)
                    continue
                elif job.status_code > 299:
                    log.error('Got status', code=job.status_code)
                    raise Exception
                for line in job.iter_lines():
                    if line:
                        line = line.strip()
                        incr('jobs')
                        obs.on_next(line.decode('utf-8'))
                continue
            except KeyboardInterrupt as ex:
                obs.on_completed()
                log.info('bye')
                return
            except Exception as ex:
                log.error('No connection, sleeping 2 secs')
                try:
                    time.sleep(2)
                except KeyboardInterrupt as ex:
                    obs.on_completed()
                    log.info('bye')
                    return
                incr('conn_err')

    active_cpes.active_cpes_maintainance()

    return (
        rx.Observable.create(jobs)
        .map(json.loads)
        .map(active_cpes.add_active)
        .filter(lambda ev: ev)
        .group_by(lambda job: job['cpeid'])
        # one greenlet per cpe:
        .flat_map(lambda s: s.observe_on(GS).map(send_cnr))
        .buffer_with_time(FLAGS.buffer_time * 1000)
        .subscribe(send_results, err)
    )


run = lambda: app.run(main)

if __name__ == '__main__':
    run()
