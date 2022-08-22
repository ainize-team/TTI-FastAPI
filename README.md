# TTI-FastAPI

Serving Text to Image Model Using FastAPI and Celery

## Docker
```shell
docker build -t tti-fast-api .
docker run -d -p 8000:8000 --gpus=all tti-fast-api
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
