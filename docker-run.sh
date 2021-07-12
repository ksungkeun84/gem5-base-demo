#!/bin/bash

sudo docker run --rm -i -t \
  --privileged \
  -p 5555:5555 \
  -p 5672:5672 \
  -v $PWD:/workspace \
  danguria/gem5art
