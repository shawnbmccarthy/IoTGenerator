import logging
from .camera import Camera
from .door import Door
from .env_sensor import EnvSensor
from .light import Light
from .solar import Solar

class SensorFactory:
    def __init__(self):
        """

        """
        self._logger = logging.getLogger(__name__)
    """
    Simple helper to build the sensor object driven from the configuration file
    """
    def get_sensor(self, sensor_name, device_id, sensor_id, sensor_type, sensor_info, polling_seconds, bucket_size):
        """

        :param sensor_name:
        :param device_id:
        :param sensor_id:
        :param sensor_type:
        :param sensor_info:
        :param polling_seconds:
        :param bucket_size:
        :return:
        """
        self._logger.info('attempting to create sensor type: {}'.format(sensor_type))
        sensor_obj = None
        if sensor_type == 'DOOR':
            sensor_obj = Door(device_id, sensor_id, sensor_name, sensor_info, polling_seconds, bucket_size)
        elif sensor_type == 'CAMERA':
            sensor_obj = Camera(device_id, sensor_id, sensor_name, sensor_info, polling_seconds, bucket_size)
        elif sensor_type == 'ENV_SENSOR':
            sensor_obj = EnvSensor(device_id, sensor_id, sensor_name, sensor_info, polling_seconds, bucket_size)
        elif sensor_type == 'LIGHT':
            sensor_obj = Light(device_id, sensor_id, sensor_name, sensor_info, polling_seconds, bucket_size)
        elif sensor_type == 'SOLAR':
            sensor_obj = Solar(device_id, sensor_id, sensor_name, sensor_info, polling_seconds, bucket_size)
        else:
            self._logger.warning('sensor object for {} type does not exist'.format(sensor_type))
        self._logger.debug('attempting ot return sensor object: {}'.format(sensor_obj))
        return sensor_obj
