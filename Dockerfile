FROM nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # VIRTUAL_ENVIRONMENT_PATH="/app/.venv"
    DEBIAN_FRONTEND=noninteractive 

ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Python3.8
RUN apt-get update && \
    apt remove python-pip  python3-pip && \
    apt-get install --no-install-recommends -y \
    build-essential \
    ca-certificates \
    curl \
    g++ \
    python3.8 \
    python3.8-dev \
    python3.8-distutils \
    python3.8-venv \
    python3-venv \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3.8 get-pip.py

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && update-alternatives --install /usr/local/bin/pip pip /usr/local/bin/pip3.8 1

RUN python3.8 -m venv /home/venv

ENV PATH="/home/venv/bin:$PATH"

RUN python -m pip install -U pip setuptools

# Install Poetry
# https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python - 

WORKDIR /app
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install --no-dev

ARG MODEL_URL="https://ommer-lab.com/files/latent-diffusion/nitro/txt2img-f8-large/model.ckpt"
ARG CONFIG_URL="https://raw.githubusercontent.com/CompVis/latent-diffusion/main/configs/latent-diffusion/txt2img-1p4B-eval.yaml"
RUN mkdir /app/model
RUN wget --no-verbose --show-progress --progress=bar:force:noscroll -O /app/model/model.ckpt ${MODEL_URL}
RUN wget --no-verbose --show-progress --progress=bar:force:noscroll -O /app/model/config.yaml ${CONFIG_URL}

COPY ./tti_fastapi/ /app/

EXPOSE 8000

COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ./start.sh