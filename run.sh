#!/usr/bin/env bash

set -e

docker run --rm -it --name zmk -v $(pwd)/firmware:/app/firmware zmk
