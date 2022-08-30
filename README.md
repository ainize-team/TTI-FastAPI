# TTI-FastAPI

Serving Text to Image Model Using FastAPI and Celery

## Docker
```shell
docker build -t tti-fast-api .
docker run -d --name tti-fastapi -p 8000:8000 \
    -e BROKER_URI=<broker_uri> \
    -e FIREBASE_DATABASE_URL=<firebase_realtime_database_url>  \
    -v <firebase_credential_dir_path>:/app/key tti-fastapi
```
## For Developers

1. install dev package.

```shell
poetry install
```

2. install pre-commit.

```shell
pre-commit install
```
