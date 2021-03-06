from datetime import datetime as dt
from ina219 import INA219
from .base_sensor import Sensor

class Solar(Sensor):
    def __init__(self, device_id, sensor_id, sensor_name, sensor_info, polling_seconds=5, bucket_size=200):
        """

        :param device_id:
        :param sensor_id:
        :param sensor_loc_name:
        :param sensor_info:
        :param polling_s:
        :param sample_size:
        """
        super(Solar, self).__init__(
            device_id,
            sensor_id,
            'SOLAR',
            sensor_name,
            sensor_info,
            polling_seconds,
            bucket_size
        )

    def setup_device(self):
        """

        :return:
        """
        self._panel_addr = INA219(
            self._sensor_info['shunt_ohms'],
            self._sensor_info['max_expected_amps'],
            address=self._sensor_info['addr']
        )

        # TODO: hardcoded: this should be ok, i guess?
        self._panel_addr.configure(
            voltage_range=self._panel_addr.RANGE_16V,
            gain=self._panel_addr.GAIN_AUTO,
            bus_adc=self._panel_addr.ADC_128SAMP,
            shunt_adc=self._panel_addr.ADC_128SAMP
        )

        self.current_state = {
            'voltage': self._panel_addr.voltage(),
            'current': self._panel_addr.current()
        }

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
        self._logger.debug('attempting to get solar data')
        return {
            'device_id': self.device_id,
            'sensor_name': self.sensor_name,
            'sensor_type': self.sensor_type,
            'sensor_id': self.sensor_id,
            'n_samples': self.get_sample_size(),
            'timestamp': dt.now(),
            'value': {
                'voltage': self._panel_addr.voltage(),
                'current': self._panel_addr.current(),
                'power': self._panel_addr.voltage() * self._panel_addr.current()
            }
        }

    def execute_cmd(self, cmd):
        """
        TODO: what to execute? get current power?

        :param cmd:
        :return:
        """
        self._logger.info('running solar sensor command')
        return self.get_sensor_data()

    def register_event(self, evt_logger):
        """

        :param evt_logger:
        :return:
        """
        pass

    def event_callback(self, evt):
        """
        TODO: Implement what? and how?

        :param evt:
        :return:
        """
        pass