#!/bin/bash
echo "Stopping and cleaning up containers..."
docker-compose down

echo "Building and starting containers..."
docker-compose up --build
