#!/bin/bash
sudo docker run -p 27017:27017 -v /data/sungkeun/mongodb:/data/db -d mongo
