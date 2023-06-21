# TTI-FastAPI

Serving Text to Image Model Using FastAPI, RabbitMQ and Celery worker

## How to start
### Using docker-compose(recommended)
1. Clone repository
```shell
git clone https://github.com/ainize-team/TTI-FastAPI
cd TTI-FastAPI
```

2. Edit [docker-compose.yml](./docker-compose.yml), [rabbitmq.env](./envs/rabbimq.env.sample) and [fastapi.env](./envs/fastapi.env.sample) for your project.

3. Run containers
```shell
docker-compose up -d
```

4. (Optional) config rabbimq user setting
```shell
docker exec tti-rabbitmq -it /bin/bash
cd scripts
./init_rabbitmq
```

### Using docker
1. Clone repository
```shell
git clone https://github.com/ainize-team/TTI-FastAPI
cd TTI-FastAPI
```

2. Build docker image
```shell
docker build -t tti-fastapi .
```

3. Create docker container
```
docker run -d --name tti-fastapi -p 8000:8000 \
    -e BROKER_URI=<broker_uri> \
    -e FIREBASE_DATABASE_URL=<firebase_realtime_database_url>  \
    -v <firebase_credential_dir_path>:/app/key tti-fastapi
```

Or, you can use the [.env file](./envs/fastapi.env.sample) to run as follows.

```shell
docker build -t tti-fastapi .
docker run -d --name tti-fastapi -p 8000:8000 \
    --env-file .env \
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
