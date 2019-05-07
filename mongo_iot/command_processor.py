import logging

from datetime import datetime as dt
from threading import Thread

class CommandProcessor(Thread):
    def __init__(self, cmd_coll, sensor_coll):
        super(CommandProcessor, self).__init__()
        self._cmd_coll = cmd_coll
        self._sensor_coll = sensor_coll
        self._is_running = True
        self._sensor_list = {}
        self._logger = logging.getLogger(__name__)
        self._resume_token = None
        self._logger.info('command proccessor setup')

    def add_sensor(self, sensor):
        self._sensor_list[sensor.sensor_id] = sensor
        self._logger.info('sensor added: {}:{}'.format(sensor.sensor_id, self._sensor_list[sensor.sensor_id].sensor_name))

    def run(self):
        """
        TODO: need to work out best way to capture command and pass to existing
        TODO: sensor object (events maybe?) not sure yet will work out later

        TODO: need to test this logic -> when do we enter the loop? etc.
        TODO: Fix this sensor current_state logic I don't like it -
        :return:
        """
        self._logger.info('command processor running')

        while self._is_running:
            try:
                #
                # TODO: What is the best way to cleanly shut down a change stream when a process is
                # TODO: shutting down?
                #
                with self._cmd_coll.watch(
                    [{'$match': {'operationType': 'insert'}}]
                ) as stream:
                    self._logger.info('command processor inside watch')
                    for doc in stream:
                        self._resume_token = doc['_id']
                        cmd_doc = doc['fullDocument']
                        sensor_id = cmd_doc['sensor_id']
                        self._logger.info('executing command for sensor id: {}'.format(sensor_id))
                        sensor = self._sensor_list[sensor_id]
                        ret_data = sensor.execute_cmd(cmd_doc['desired_state'])
                        try:
                            self._sensor_coll.update_one(
                                {
                                    'sensor_name': sensor.sensor_name,
                                    'sensor_type': sensor.sensor_type,
                                    'sensor_id': sensor.sensor_id
                                },
                                {
                                    '$set': {
                                        'current_state': ret_data['value'],
                                        'last_updated': dt.now()
                                    }
                                }
                            )
                        except Exception as e:
                            self._logger.error('problem processing sensor command: {}, error: {}'.format(sensor.sensor_name, e))
            except Exception as e:
                    self._logger.error('problem running command: {}'.format(e))

    def stop(self):
        """

        :return:
        """
        self._is_running = False
