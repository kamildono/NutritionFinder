#!/bin/bash

if [ "$1" == "--rebuild" ]; then
  docker-compose down
  docker-compose up --build
else
  docker-compose up
fi
