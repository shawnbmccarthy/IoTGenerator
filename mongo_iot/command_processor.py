import logging

from datetime import datetime as dt
from threading import Thread

class CommandProcessor(Thread):
    def __init__(self, cmd_coll, sensor_coll):
        self._cmd_coll = cmd_coll
        self._sensor_coll = sensor_coll
        self._is_running = True
        self._sensor_list = {}
        self._logger = logging.getLogger(__name__)
        self._resume_token = None

    def add_sensor(self, sensor):
        self._sensor_list[sensor.sensor_id] = sensor

    def run(self):
        """
        TODO: need to work out best way to capture command and pass to existing
        TODO: sensor object (events maybe?) not sure yet will work out later

        TODO: need to test this logic -> when do we enter the loop? etc.
        TODO: Fix this sensor current_state logic I don't like it -
        :return:
        """
        try:
            while self._is_running:
                with self._cmd_coll.watch(
                    [{'$match': {'operationType': 'insert'}}]
                ) as stream:
                    for doc in stream:
                        self._resume_token = doc['_id']
                        cmd_doc = doc['fullDocument']
                        sensor = cmd_doc['sensor_id']
                        value = sensor.execute_cmd(cmd_doc['desired_state'])
                        try:
                            self._sensor_coll.update_one(
                                {
                                    'sensor_name': sensor.sensor_name,
                                    'sensor_type': sensor.sensor_type,
                                    'sensor_id': sensor.sensor_id
                                },
                                {
                                    '$set': {
                                        'current_state': value.current_state,
                                        'last_updated': dt.now()
                                    }
                                }
                            )
                        except Exception as e:
                            self._logger.error('problem processing sensor command: {}, error: {}'.format(sensor.sensor_name, e))
                        pass
        except Exception as e:
            self._logger.error('problem running command: {}'.format(e))

    def stop(self):
        """

        :return:
        """
        self._is_running = False
