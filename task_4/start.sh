#!/bin/bash

set -e

cd "$(dirname "$0")"

docker rm -f parser-service postgres-db || true

docker network create parser-net 2>/dev/null || true

docker run -d \
  --name postgres-db \
  --network parser-net \
  -e POSTGRES_DB=hh_parser \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15-alpine

sleep 5

docker build -t github-parser-app .

docker run -d \
  --name parser-service \
  --network parser-net \
  -p 8000:8000 \
  --env-file .env \
  github-parser-app

docker logs -f parser-service