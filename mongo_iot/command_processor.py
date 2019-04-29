import logging

from threading import Thread

class CommandProcessor(Thread):
    def __init__(self, cmd_coll):
        self._cmd_coll = cmd_coll
        self._is_running = True
        self._sensor_list = {}
        self._logger = logging.getLogger(__name__)

    def add_sensor(self, sensor):
        self._sensor_list[sensor.sensor_id] = sensor

    def run(self):
        """
        TODO: need to work out best way to capture command and pass to existing
        TODO: sensor object (events maybe?) not sure yet will work out later
        :return:
        """
        try:
            while self._is_running:
                with self._cmd_coll.watch(
                    [{'$match': {'operationType': 'update'}}]
                ) as stream:
                    for doc in stream:
                        # look for updates - self._sensor_list[_id]
                        pass
        except Exception as e:
            self._logger.error('problem running command: {}'.format(e))

    def stop(self):
        self._is_running = False
