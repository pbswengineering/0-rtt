#!/usr/bin/env bash
cd "$(dirname "$(realpath -- "$0")")/../containers"
pwd
docker compose up