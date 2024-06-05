#!/bin/bash

cd /home

python3 -m pytest --cov-report term --cov=app --cov=rabbit_helper  tests/integration_tests.py -rP