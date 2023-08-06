#!/usr/bin/env python
from __future__ import print_function

"""
'Inside Out' HTTP CNR Proxy


USAGE: proxy [AX1 URL]  [AX2 URL] ...

EXAMPLE: proxy https://A1.axiros.com/CNR

---

DETAILS: https://axc2.axiros.com/maxmd/HTTPCNRProxy

Opens http long polling connections to http(s) servers (given on CLI) and starts
receiving CNR jobs, which it processes, grouped by cpeids, concurrently.

In small intervals we post results back to the servers, syncronously.

"""

__author__ = 'Gunther Klessinger, Axiros GmbH, Germany'


import os, json, sys, time, traceback

env, argv = os.environ.get, sys.argv[1:]
cfg = {}
"""
    "servers": argv if argv,
    "cnr_timeout": env("CNR_TIMEOUT", 2),
    "log_level": env("LOG_LEVEL", 10),
}
"""

# Non Stdlib Packages:
try:
    # We use ReactiveX for orchestration...
    import rx

    # ... and greenlets for async/concurrency
    from gevent import monkey

    monkey.patch_all()

    # Simple logging to stdout:
    import requests, structlog
except ImportError as ex:
    print(str(ex))
    print('pip install gevent structlog requests rx')
    sys.exit(1)


from requests.auth import HTTPDigestAuth as digest
from threading import current_thread

tn = lambda: current_thread().name


logger = structlog.get_logger()


def log(lev, msg, **kw):
    if lev < cfg['log_level']:
        return
    kw['tn'] = tn()
    kw['level'] = (
        'debug'
        if lev < 11
        else 'info'
        if lev < 21
        else 'warning'
        if lev < 31
        else 'error'
    )
    logger.msg(msg, **kw)


def err(exc):
    f = traceback.format_exc()
    log(30, 'Stream Exception', exc=str(exc), tb=f)
    return exc


GS = rx.concurrency.GEventScheduler()
concurrent = lambda stream: stream.subscribe_on(GS)


def send_cnr(cnr):
    log(10, 'Sending', **cnr)
    t0 = time.time()
    res = {'cpeid': cnr['cpeid']}
    try:
        req = requests.get(
            cnr['url'],
            auth=digest(cnr.get('user', ''), cnr.get('password', '')),
            timeout=cnr.get('timeout', cfg['cnr_timeout']),
        )
        res['status'] = req.status_code
    except requests.exceptions.Timeout:
        res['status'] = 504
    except Exception as ex:
        res['status'] = 599
        res['details'] = str(ex)
    res['dt'] = int((time.time() - t0) * 1000)
    log(20, 'Got CNR Result', **res)
    return res


def send_results(s):
    log(20, 'sending results', s=s)


def foo(s):
    return s.observe_on(GS).map(send_cnr)


def get_poll_stream(ax_url):
    def jobs(obs, url=ax_url):
        while True:
            # FIXME sending all the time? What if tail -f ? is the job ?
            try:
                job = requests.get(url, stream=True)
                for line in job.iter_lines():
                    if line:
                        line = line.strip()
                        obs.on_next(line.decode('utf-'))
                continue
            except KeyboardInterrupt as ex:
                info('bye')
                return
            """
            except Exception as ex:
                print("no connection", ex)
                time.sleep(2)
            """

    return (
        rx.Observable.create(jobs)
        .map(json.loads)
        .group_by(lambda job: job['cpeid'])
        .flat_map(lambda s: foo(s))
        .buffer_with_time(2000)
        .subscribe(send_results, err)
    )


def main(argv):
    print('main')
    return
    (
        rx.Observable.from_(urls)
        .map(
            lambda u: 'http://127.0.0.1%s' % u
            if u.startswith(':')
            else u
            if u.startswith('http')
            else 'http://%s' % u
        )
        .map(get_poll_stream)
        .map(lambda o: None)
        .subscribe(print, err)
    )


from absl import app


def run():
    app.run(main)


if __name__ == '__main__':
    run()
    sys.exit(0)

    if len(sys.argv) == 1:
        print('start me with a full id as argument - this is my id')
        print('cli is the argument to get interactive console')
        sys.exit(1)
    fid = sys.argv[1]
    if fid == 'cli':
        have_cli = True
        from blessed import Terminal

        ap.cli.start(Terminal())
    main(sys.argv[1:])
