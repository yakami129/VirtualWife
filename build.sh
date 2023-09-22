#!/bin/bash
docker rmi okapi0129/virtualwife-chatbot
docker rmi okapi0129/virtualwife-chatvrm
docker rmi okapi0129/virtualwife-gateway
docker buildx bake -f docker-compose.build.hcl --load