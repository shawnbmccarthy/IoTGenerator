# IoT Demonstration

This will include:
1. pyspark module
1. pi to atlas
1. web app
1. mobile app

## Notes
Can only run on raspberry pi

## to run
1. move iot.sample.yml to iot.yml
1. add mongodb data to datbase configuration entry in yml file
1. update sensor info as needed
1. `python3 ./demo.py` 

## TODO:
1. finish
    1. commands
    1. events
1. add requirements.txt
1. document

## Enhancements
1. remove pi requirement from sensors
1. remove mongo requirement/database requirement from processors
1. introduce a dummy device for testing sensors without running on pi
1. enhance event processing
    1. event chain -> IFTTT type processing
    1. event logging -> make richer event capturing
1. command processing
    1. command chain -> IFTTT type processing, i.e. media_mode -> dim lights turn on tv