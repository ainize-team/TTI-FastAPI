FROM python:3.9

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PROJECT_NAME="TTI-FastAPI"

ENV PATH="$POETRY_HOME/bin:/workspaces/$PROJECT_NAME/.venv/bin:$PATH"

# Install Poetry
# https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    git \
    openssh-client \
    && curl -sSL https://install.python-poetry.org | python3 - 