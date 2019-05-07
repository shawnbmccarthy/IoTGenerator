import logging.config
import mongo_iot
import yaml

from datetime import datetime as dt

from mongo_iot.devices import SensorFactory
from mongo_iot.timeseries_processor import SensorPolling
from mongo_iot.command_processor import CommandProcessor
from mongo_iot.event_processor import EventDatabaseLogger
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

    mongo_iot.init()
    sensorFactory = SensorFactory()

    polling_sensors = []

    # TODO: remove hardcoded collections?
    client = MongoClient(cfg['database'])
    db = client.get_database()
    sensor_ts_coll = db['sensor_ts']
    sensor_coll = db['sensor']
    event_coll = db['events']
    commands_coll = db['commands']

    command_processor = CommandProcessor(commands_coll, sensor_coll)
    evtDbLogger = EventDatabaseLogger(event_coll)

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
            logger.info('adding {} to commands'.format(sensor.sensor_name))
            command_processor.add_sensor(sensor)

        if events:
            logger.info('{} registering event'.format(sensor.sensor_name))
            sensor.register_event(evtDbLogger)

        polling_sensors.append(SensorPolling(sensor_ts_coll, sensor))

    for poller in polling_sensors:
        poller.start()

    command_processor.start()
