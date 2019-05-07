import logging


class EventLogger(object):
    def __init__(self):
        self._evt_logger = logging.getLogger(__name__)

    def emit_event(self, evt):
        self._evt_logger.info('event captured: {}'.format(evt))


class EventDatabaseLogger(EventLogger):
    def __init__(self, evt_coll):
        super(EventDatabaseLogger, self).__init__()
        self._evt_coll = evt_coll

    def emit_event(self, evt):
        super(EventDatabaseLogger,self).emit_event(evt)
        try:
            self._evt_coll.insert_one(evt)
        except Exception as e:
            self._evt_logger.error('error inserting occurred: {}'.format(e))
