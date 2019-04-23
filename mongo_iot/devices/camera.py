from datetime import datetime as dt
from io import BytesIO
from picamera import PiCamera
from time import sleep
from .base_sensor import Sensor

import base64

class Camera(Sensor):
    def __init__(self, device_id, sensor_id, sensor_name, sensor_info, polling_seconds=10, bucket_size=40):
        """

        :param device_id:
        :param sensor_id:
        :param sensor_name:
        :param sensor_info:
        :param polling_seconds:
        :param bucket_size:
        """
        super(Camera, self).__init__(
            device_id, sensor_id,
            'CAMERA',
            sensor_name,
            sensor_info,
            polling_seconds,
            bucket_size
        )
        self._camera = None

    def _take_picture(self):
        """

        :return:
        """
        stream = BytesIO()
        self._camera.start_preview()
        sleep(3)
        self._camera.capture(stream, 'jpeg')
        value = base64.b64encode(base64.b64encode(stream.getvalue()))
        stream.close()
        self._camera.stop_preview()
        return value

    def setup_device(self):
        """

        :return:
        """
        self._camera = PiCamera()
        self._camera.resolution = (640, 480)
        self._camera.rotation = 0
        self.current_state = self._take_picture()
        return {
            'sensor_name': self.sensor_name,
            'sensor_type': self.sensor_type,
            'sensor_id': self.sensor_id,
            'current_state': self.current_state
        }

    def get_sensor_data(self):
        """

        :return:
        """
        self._logger.debug('attempting to get sensor data')
        return {
            'device_id': self.device_id,
            'sensor_name': self.sensor_name,
            'sensor_type': self.sensor_type,
            'sensor_id': self.sensor_id,
            'n_samples': self.get_sample_size(),
            'timestamp': dt.now(),
            'value': self._take_picture()
        }