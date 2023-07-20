#!/bin/bash
docker rmi virtualwife/gateway
docker rmi virtualwife/chatbot
docker rmi virtualwife/chatvrm
docker buildx bake -f docker-compose.build.yaml