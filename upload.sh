#!/bin/bash

# 定义版本号变量
VERSION="v2.0.3"

# 打标签并推送镜像
docker buildx bake -f docker-compose.build.hcl chatbot-release chatvrm-release gateway-release --set target.args.TAG=$VERSION  --push
