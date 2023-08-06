"""
Stdlib Free Fast Logging, Using Structlog Only

Usage:
    axlog.setup_logging()  once per app
    axlog.get_logger('axwifi').info('foo', bar=baz)

    The app may use falgs: --log_level=20
"""


import structlog
import sys

# -- Setup for a stdlib logging free, getattr free use:
from structlog.processors import JSONRenderer
from structlog import BoundLoggerBase, PrintLogger, wrap_logger
from structlog import wrap_logger
from structlog.exceptions import DropEvent
from absl import flags
from threading import current_thread
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter, Terminal256Formatter

flags.DEFINE_integer('log_level', 20, 'Log level')

# fmt:off
log_levels = {
    'fatal'     : 70,
    'critical'  : 60,
    'error'     : 50,
    'exception' : 50,
    'err'       : 50,
    'warn'      : 40,
    'warning'   : 40,
    'info'      : 20,
    'debug'     : 10,
}
# fmt:on


class AXLogger(BoundLoggerBase):
    """A Bound Logger is a concrete one, e.g. stdlib logger"""

    def log(self, event, kw, method):
        try:
            args, kw = self._process_event(method, event, kw)
        except DropEvent:
            return
        return self._logger.msg(*args, **kw)


for l, nr in log_levels.items():
    setattr(AXLogger, l, lambda self, ev, meth=l, **kw: self.log(ev, kw, meth))


def get_logger(name, level=None, **ctx):
    """supports name and level conventions - matches the processor chain"""
    if not structlog.is_configured():
        setup_logging()

    level = level or flags.FLAGS.log_level
    log = wrap_logger(PrintLogger(), wrapper_class=AXLogger)
    log._logger.name = name
    log._logger.level = level
    return log.bind(**ctx)


def filter_by_level(logger, meth, ev):
    if log_levels[meth] < logger.level:
        raise DropEvent
    return ev


class ConsoleRender(structlog.dev.ConsoleRenderer):
    pygmentize = ('results',)

    def __call__(self, _, __, ev):
        pygm = {}
        for k in self.pygmentize:
            v = ev.pop(k, None)
            if v:
                pygm[k] = v

        line = structlog.dev.ConsoleRenderer.__call__(self, _, __, ev)
        if pygm:
            line += '\n' + prettyjson(pygm)

        return line


def prettyjson(j):
    sj = json.dumps(j, indent=4, default=str)
    hl = highlight(sj, JsonLexer(), Terminal256Formatter(style='tango'))
    return hl


def censor_passwords(_, __, ev):
    pw = ev.get('password')
    if pw:
        ev['password'] = pw[:3] + '*' * (len(pw) - 3)
    return ev


if sys.stdout.isatty():
    renderer = ConsoleRender()
else:
    renderer = JSONRenderer()

std_processors = [
    filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    censor_passwords,
    structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S'),
    structlog.processors.StackInfoRenderer(),
    renderer,
]


def setup_logging(processors=None):
    structlog.configure(
        processors=processors or std_processors,
        context_class=dict,
        wrapper_class=AXLogger,
        cache_logger_on_first_use=True,
    )
