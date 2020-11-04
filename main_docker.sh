#!/bin/bash

if [ ! -d tmp ]; then
  mkdir tmp
fi

# see https://docs.docker.com/engine/reference/run/
# run the container with full host permissions
docker run \
        --rm \
        --privileged \
        --cap-add="ALL" \
        --pid="host" \
        --uts="host" \
        --ipc="host" \
        --network="host"\
        -v "$PWD"/tmp:/root/peracotta/tmp \
        -it peracotta
