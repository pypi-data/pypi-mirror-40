from ...events import Event
from ...plugins import PapersPlugin


class LogPlugin(PapersPlugin):

    name = 'log'

    def __init__(self, conf):
        if 'log' in conf['plugins'] and 'path' in conf['plugins']['log']:
            logfile = conf['plugins']['log']['path']
        else:
            logfile = None  # TODO
        logger = None # TODO

    @Event.listener
    def log(self, event):
        self.logger.info(str(event))
