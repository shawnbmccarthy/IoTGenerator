"""

"""
import logging

from threading import Timer


class SensorPolling(object):
    """
    Responsible for running sensor object
    """
    def __init__(self, coll, sensor_obj):
        self._timer = None
        self.coll = coll
        self.sensor_obj = sensor_obj
        self._logger = logging.getLogger(__name__)
        self.running = False
        self.start()

    def _run(self):

        data = self.sensor_obj.get_sensor_data()
        try:
            self.coll.update_one(
                {
                    'device_id': data['device_id'],
                    'sensor_name': data['sensor_name'],
                    'sensor_type': data['sensor_type'],
                    'sensor_id': data['sensor_id'],
                    'n_samples': {'$lt': data['n_samples']},
                    'day': data['timestamp'].replace(hour=0, minute=0, second=0, microsecond=0)
                },
                {
                    '$set': {
                        'last': data['timestamp'],
                    },
                    '$inc': {
                        'n_samples': 1
                    },
                    '$push': {
                        'samples': {'timestamp': data['timestamp'], 'value': data['value']}
                    },
                    '$setOnInsert': {
                        'first': data['timestamp']
                    }
                },
                upsert=True
            )
        except Exception as e:
            self._logger.error('update failed: {}'.format(e))

        # move here to make sure we only start another run after the sensor collection completes
        self.running = False
        self.start()

    def start(self):
        if not self.running:
            self._timer = Timer(self.sensor_obj.get_polling_interval(), self._run)
            self._timer.start()
            self.running = True

    def stop(self):
        self._timer.cancel()
        self.running = False
