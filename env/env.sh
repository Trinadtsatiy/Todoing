#! /bin/bash

# JWT settings
export JWT_SECRET_KEY=secret
export JWT_ALGORITHM=HS256
export JWT_EXPIRES_IN=2

# PostgreSQL settings
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

# Server settings
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8000