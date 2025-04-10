  #!/bin/bash

if ! [ $1 ]; then
    echo "> Missing path to data directory!"
    exit
fi
DATA_PATH=$1

nvidia-docker run \
  -v $DATA_PATH:/workspace/data \
  -it piotrekwoznicki/adpkd-net:v0.1
