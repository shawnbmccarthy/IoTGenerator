import logging.config
import yaml

from datetime import datetime as dt
from mongo_iot.devices import SensorFactory
from mongo_iot.timeseries_processor import SensorPolling
from pymongo import MongoClient


def setup_logging():
    """
    TODO: Hardcoded right now, fix maybe?

    :return:
    """
    with open('./logging.yml', 'r') as l:
        l_cfg = yaml.load(l, Loader=yaml.SafeLoader)
    logging.config.dictConfig(l_cfg)


if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)

    with open('./iot.yml', 'r') as yml_cfg:
        cfg = yaml.load(yml_cfg, Loader=yaml.SafeLoader)

    sensorFactory = SensorFactory()
    polling_sensors = []

    # TODO: remove hardcoded collections?
    client = MongoClient(cfg['database'])
    db = client.get_database()
    sensor_ts_coll = db['sensor_ts']
    sensor_coll = db['sensor']
    commands_coll = db['commands']

    for sensor_cfg in cfg['sensors']:
        logger.info('setting up {} sensor'.format(sensor_cfg['name']))
        sensor = sensorFactory.get_sensor(
            sensor_cfg['name'],
            sensor_cfg['device_id'],
            sensor_cfg['id'],
            sensor_cfg['type'],
            sensor_cfg['sensor_info'],
            sensor_cfg['polling_seconds'],
            sensor_cfg['bucket_size']
        )
        sensor.setup_device()
        try:
            sensor_coll.update_one(
                {
                    'sensor_name': sensor.sensor_name,
                    'sensor_type': sensor.sensor_type,
                    'sensor_id': sensor.sensor_id
                },
                {
                    '$set': {
                        'current_state': sensor.current_state,
                        'last_updated': dt.now()
                    },
                    '$setOnInsert': {
                        'created_on': dt.now()
                    }
                },
                upsert=True
            )
        except Exception as e:
            logger.error('problem updating sensor state: {}, error: {}'.format(sensor.sensor_name, e))

        commands = sensor_cfg.get('commands', None)
        events = sensor_cfg.get('events', None)
        if commands:
            logger.info('attempting to setup commands')
            pass

        if events:
            logger.info('attempting to setup events')
            pass
        polling_sensors.append(SensorPolling(sensor_ts_coll, sensor))

    for poller in polling_sensors:
        poller.start()
