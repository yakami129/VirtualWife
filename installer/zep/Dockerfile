# Dockerfile
FROM okapi0129/getzep-zep-nlp-server:latest AS build

FROM python:3.11

WORKDIR /app

COPY --from=build /app /app
COPY --from=build /root/.cache/torch/sentence_transformers/moka-ai_m3e-base /root/.cache/torch/sentence_transformers/moka-ai_m3e-base
ENV VIRTUAL_ENV=/app/.venv PATH=/app/.venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

EXPOSE 3000
CMD ["python", "main.py"]