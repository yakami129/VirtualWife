#!/bin/bash
# 打标签并推送镜像
docker buildx bake -f docker-compose.build.hcl chatbot-release chatvrm-release gateway-release --push
