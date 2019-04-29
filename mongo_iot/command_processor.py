import logging

from threading import Thread
from .devices import SensorFactory

class CommandProcessor(Thread):
    def __init__(self, cmd_coll):
        self._cmd_coll = cmd_coll
        self._is_running = True
        self._factory = SensorFactory()
        self._logger = logging.getLogger(__name__)

    def run(self):
        """
        TODO: need to work out best way to capture command and pass to existing
        TODO: sensor object (events maybe?) not sure yet will work out later

        :return:
        """
        while self._is_running:
            try:
                with self._cmd_coll.watch(
                    [{'$match': {'operationType': 'update'}}],
                    full_document='updateLookup'
                ) as stream:
                    for doc in stream:
                        pass
            except Exception as e:
                self._logger.error('failed to process command: {}'.format(e))

    def stop(self):
        self._is_running = False
