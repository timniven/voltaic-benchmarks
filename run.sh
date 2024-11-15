#!/bin/bash

docker run \
    --rm \
    --platform linux/amd64 \
    -p "8501:8501" \
    -v ${PWD}:/voltaic \
    -w /voltaic \
        timniven/voltaic:latest \
            streamlit run dashboard.py
