#!/bin/bash
docker buildx build --platform linux/amd64,linux/arm64 -t okapi0129/getzep-zep-nlp-server:v1.0.0 . --push

