#!/bin/bash

# 定义版本号变量
VERSION="v2.0.0"

# 打标签并推送镜像
docker tag okapi0129/virtualwife-chatbot:latest okapi0129/virtualwife-chatbot:$VERSION
docker tag okapi0129/virtualwife-chatvrm:latest okapi0129/virtualwife-chatvrm:$VERSION
docker tag okapi0129/virtualwife-gateway:latest okapi0129/virtualwife-gateway:$VERSION

docker push okapi0129/virtualwife-chatbot:$VERSION
docker push okapi0129/virtualwife-chatvrm:$VERSION
docker push okapi0129/virtualwife-gateway:$VERSION
