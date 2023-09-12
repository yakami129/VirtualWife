#!/bin/bash
docker rmi okapi0129/virtualwife-chatbot
docker rmi okapi0129/virtualwife-chatvrm
docker rmi okapi0129/virtualwife-gateway
docker buildx create --use
docker buildx bake -f docker-compose.build.yaml --set *.platform=linux/amd64,linux/arm64/v8