#!/usr/bin/env python
import gevent
from gevent import monkey, select, os as gevent_os

monkey.patch_all()
from bottle import response, request, Bottle, abort
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import json, requests, os, time, rx, attr, sys, structlog
import axlog
import base64
from absl import app as abslapp
from absl import flags
from ast import literal_eval

log = structlog.get_logger('cnr_server')
here = os.path.dirname(os.path.abspath(__file__))

FLAGS = flags.FLAGS
flags.DEFINE_string('bind_ip', '127.0.0.1', 'Bind IP')
flags.DEFINE_integer('bind_port', 8089, 'Bind Port')
flags.DEFINE_string('pidfile', here + '/var/server.pid', 'PidFile')
flags.DEFINE_string(
    'playbook',
    'testserver',
    'Playbook in assets dir (defining jobs to deliver)',
)
flags.DEFINE_float(
    'speed', 1.0, 'Factor to divide sleep as set in playbooks with'
)
flags.DEFINE_integer('loops', 1, 'Playbook loops')
flags.DEFINE_boolean('debug', False, 'Debug Mode')

O = rx.Observable
app = Bottle()
GS = rx.concurrency.GEventScheduler()

pass_ = lambda ev: 0
dbg = lambda: FLAGS.debug


def err(exc):
    print('Exc!!', exc)
    breakpoint()


def get_basic_auth_creds():
    try:
        auth = request.headers['Authorization'].split(' ', 1)[1]
        return base64.b64decode(auth).decode('utf-8').split(':', 1)
    except:
        return '', ''


@app.route('/fake_cnr/<cpeid>/<user>/<password>')
def fake_cpe_cnr(cpeid, user, password):
    """ just a test fake cpe cnr url (back to the server)"""
    log.debug('Fake CNR', **locals())
    sleep = request.query.get('sleep', 0)
    if sleep:
        log.debug('Sleeping', dt=sleep)
        time.sleep(float(sleep) / 1000.0)
    u, p = get_basic_auth_creds()
    if u == user and p == password:
        return cpeid
    response.status = 401
    return 'Unauthorized'


@app.route('/results', method='POST')
def results():
    r = request.body.read()
    res = json.loads(r)
    log.info('got results', results=res)
    return 'ok'


@app.route('/poll', method=('POST', 'GET'))
def longpoll():
    log.info('Long poll session start')
    u, p = get_basic_auth_creds()
    if users.get(u) != p:
        log.info('Unauthorized', user=u)
        response.status = 401
        return 'Unauthorized'
    log.info('Connected', user=u)

    i = 0
    for loop in range(FLAGS.loops):
        log.debug('Running playbook', loops=loop + 1)
        for play in playbook:
            i += 1
            if isinstance(play, (float, int)):
                time.sleep(play / FLAGS.speed)
                continue

            m = dict(play)
            m['nr'] = i
            m['url'] = m['url'].replace(
                'TESTSERVER', '%s:%s' % (FLAGS.bind_ip, FLAGS.bind_port)
            )
            j = json.dumps(m)
            yield j + '\r\n\r\n'
    log.warn('Done, standing still')
    time.sleep(1000000)  # client reconnects should we return


playbook = []

users = {}


def load_accounts():
    fn = here + '/accounts.json'
    if not os.path.exists(fn):
        log.exception('Missing accounts file', fn=fn)
        sys.exit(1)
    with open(here + '/accounts.json') as fd:
        users.update(json.loads(fd.read()))


def setup():
    global log
    load_accounts()
    if FLAGS.debug:
        FLAGS.log_level = 10
    axlog.setup_logging()
    log = axlog.get_logger('test_server')


def main(argv):
    del argv
    setup()
    fn = here + '/assets/testserver_playbooks/%s.py' % FLAGS.playbook
    log.info('Reading playbook', file=fn)
    with open(fn) as fd:
        # we wanted a python format for autoformatting and comments, so:
        s = literal_eval('[' + fd.read().split(' = [', 1)[1].strip())
    playbook.extend(s)
    log.info('Have urls', count=len(s))
    with open(FLAGS.pidfile, 'w') as fd:
        fd.write(str(os.getpid()))

    h = (FLAGS.bind_ip, FLAGS.bind_port)
    server = gevent.pywsgi.WSGIServer(
        h, app
    )  # , handler_class=WebSocketHandler)
    server.logger = log
    server.quiet = True
    log.info('CNR testserver is serving ', host=h[0], port=h[1])
    server.serve_forever()


if __name__ == '__main__':
    abslapp.run(main)
