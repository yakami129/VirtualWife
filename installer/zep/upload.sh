#!/bin/bash
# 打标签并推送镜像
docker buildx bake -f docker-compose.build.hcl postgres-release zep-release zep-nlp-server-release  --push
