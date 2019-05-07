from datetime import datetime as dt
import logging

from abc import ABC, abstractmethod

class Sensor(ABC):
    """
    The Sensor class will simply hold the data for the given sensor and provide the methods needed
    to allow the higher level classes to pull data and send update the datasource as needed

    The senor class will also provide the ability to cache data until it is confirmed it has been flushed
    as well as hold the previous 5 hours of samples
    """
    def __init__(self, device_id, sensor_id, sensor_type, sensor_name, sensor_info, polling_seconds=5, bucket_size=200):
        """

        :param device_id:
        :param sensor_id:
        :param sensor_type:
        :param sensor_name:
        :param sensor_info:
        :param polling_s: seconds in polling
        """
        self.first = None
        self.last = None
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_name = sensor_name
        self.current_state = None
        self._polling_seconds = polling_seconds
        self._bucket_size = bucket_size
        self._sensor_info = sensor_info
        self._logger = logging.getLogger(__name__)
        self._evt_logger = None
        super().__init__()

    def __getitem__(self, key):
        """

        :param key:
        :return:
        """
        return self.__dict__[key]

    def __contains__(self, key):
        """

        :param key:
        :return:
        """
        return key in self.__dict__

    def __len__(self):
        """

        :return:
        """
        return len(self.__dict__)

    def __repr__(self):
        """

        :return:
        """
        return repr(self.__dict__)

    def to_dict(self):
        """

        :return:
        """
        return {k:v for (k,v) in self.__dict__.items() if not k.startswith('_')}

    def get_polling_interval(self):
        """

        :return:
        """
        return self._polling_seconds

    def get_sample_size(self):
        """

        :return:
        """
        return self._bucket_size

    @abstractmethod
    def setup_device(self):
        """

        :return:
        """
        raise NotImplemented('Base Sensor has nothing to setup')

    @abstractmethod
    def get_sensor_data(self):
        """

        :return:
        """
        raise NotImplemented('Base Sensor class has nothing to executed')

    @abstractmethod
    def execute_cmd(self, cmd):
        """
        the base sensor has not commands to execute

        :return:
        """
        raise NotImplemented('Base sensor class has no commands({}:NotSupported)'.format(cmd))

    @abstractmethod
    def register_event(self, evt_logger):
        """

        :param evt_logger:
        :return:
        """
        raise NotImplemented('Base sensor calls has not ability to register for events')

    @abstractmethod
    def event_callback(self, evt):
        """

        :param evt:
        :return:
        """
        raise NotImplemented('Base sensor class nos ne events: Not Supported')