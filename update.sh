#!/bin/bash
git pull && \
docker compose down && \
# docker system prune -af && \
docker compose down && \
docker compose build && \
docker compose up -d && \
docker compose logs -f

