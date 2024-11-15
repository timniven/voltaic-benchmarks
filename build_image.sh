#!/bin/bash

docker build \
    --platform linux/amd64 \
    -t timniven/voltaic:latest \
    .
