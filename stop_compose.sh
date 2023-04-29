#!/bin/sh

docker compose down -v

docker rmi core-service:latest auth-service:latest