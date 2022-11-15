# mlflow

## Setup

1. run `docker build - < DockerFile --rm --tag mlflow`
2. run `docker-compose up`
3. go to `http://localhost:8080`

## Clean

1. run `docker-compose rm mlflow`
2. run `rm -rf docker/`

## Issues

- Swap sqlite3 for PostgreSQL
