#!/bin/bash

# Set default values if environment variables are not set
PORT="${PORT:-8000}"
# Remove any spaces from API_PREFIX
API_PREFIX=$(echo "${API_PREFIX:-/api}" | tr -d ' ')

# Start the application using main.py
cd /app/src && python main.py 