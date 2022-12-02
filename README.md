# TTI-FastAPI

Serving Text to Image Model Using FastAPI and Celery

## Installation
1. build docker image
```shell
git clone https://github.com/ainize-team/TTI-FastAPI
cd TTI-FastAPI
docker build -t tti-fast-api .
```

2. Run Docker Image
```
docker run -d --name tti-fastapi -p 8000:8000 \
    -e BROKER_URI=<broker_uri> \
    -e FIREBASE_DATABASE_URL=<firebase_realtime_database_url>  \
    -v <firebase_credential_dir_path>:/app/key tti-fastapi
```

Or, you can use the [.env file](./.env.sample) to run as follows.

```shell
docker build -t tti-fast-api .
docker run -d --name tti-fastapi -p 8000:8000 \
     --env-file {.env_file_path} \
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
