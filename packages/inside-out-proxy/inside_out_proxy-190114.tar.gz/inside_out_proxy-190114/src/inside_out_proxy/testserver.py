#!/usr/bin/env python
import gevent
from gevent import monkey, select, os as gevent_os

monkey.patch_all()
from bottle import request, Bottle, abort
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import json, requests, os, time, rx, attr, sys, structlog
from absl import app as abslapp
from absl import flags

log = structlog.get_logger('cnr_server')
here = os.path.dirname(os.path.abspath(__file__))

FLAGS = flags.FLAGS
flags.DEFINE_string('bind_ip', '127.0.0.1', 'Bind IP')
flags.DEFINE_integer('bind_port', 8089, 'Bind Port')
flags.DEFINE_string('pidfile', here + '/var/server.pid', 'PidFile')
flags.DEFINE_boolean('debug', False, 'Debug Mode')

O = rx.Observable
app = Bottle()
GS = rx.concurrency.GEventScheduler()

pass_ = lambda ev: 0
dbg = lambda: FLAGS.debug


def err(exc):
    print('Exc!!', exc)
    breakpoint()


@app.route('/test_cpe_cnr/<cpeid>')
def fake_cpe_cnr(cpeid):
    """ just a test fake cpe cnr url (back to the server)"""
    FLAGS.debug and log.debug('Fake CNR', cpe=cpeid)

    if cpeid == 'two':
        print('!!')
        time.sleep(10)
    return cpeid


@app.route('/', method=('POST', 'GET'))
def longpoll():
    log.info('Long poll session start')
    i = 0
    cpe = 'one'
    while True:
        i += 1
        time.sleep(0.5)
        m = {
            'nr': i,
            'cpeid': cpe,
            'url': 'http://127.0.0.1:8083/cnr/%s' % cpe,
        }
        cpe = 'two' if cpe == 'one' else 'one'
        j = json.dumps(m)
        yield j + '\r\n\r\n'
        time.sleep(0)


def main(argv):
    del argv
    with open(FLAGS.pidfile, 'w') as fd:
        fd.write(str(os.getpid()))

    h = (FLAGS.bind_ip, FLAGS.bind_port)
    server = gevent.pywsgi.WSGIServer(h, app, handler_class=WebSocketHandler)
    log.info('CNR sender is serving ', host=h[0], port=h[1])
    server.serve_forever()


if __name__ == '__main__':
    abslapp.run(main)
