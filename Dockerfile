FROM python:3.11-slim-buster AS build

LABEL org.opencontainers.image.source="https://github.com/grai-io/grai-actions"


ARG PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    PYTHONFAULTHANDLER="1" \
    PYTHONHASHSEED="random" \
    PIP_NO_CACHE_DIR="off" \
    PIP_DISABLE_PIP_VERSION_CHECK="on" \
    PIP_DEFAULT_TIMEOUT="100" \
    POETRY_VERSION="1.3.1"

# libpq-dev, and gcc are reuired for psycopg2.
RUN apt update \
    && apt install -y \
    apt-utils \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./grai-actions /grai-actions
COPY ./grai-actions/entrypoints /entrypoints
WORKDIR /grai-actions

# I'm a little unclear why the second install is required. It
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false  \
    && poetry lock --no-update \
    && poetry install --no-interaction --no-ansi --only main \
    && rm -rf ~/.cache/pypoetry/cache \
    && rm -rf ~/.cache/pypoetry/artifacts


ENTRYPOINT ["/entrypoints/entrypoint.sh"]
