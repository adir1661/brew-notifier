FROM python:3.10-slim

WORKDIR  /brew-notifier

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1\
    POETRY_VERSION=1.1.13 \
    DOCKERIZE_VERSION=v0.6.1 \
    TINI_VERSION=v0.19.0

RUN apt-get update -y && apt-get install -y wget \
    git \
    python3-dev \
    python-psycopg2 \
    libssl-dev \
    libcurl4-openssl-dev

RUN python -m pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

ARG CODEARTIFACT_AUTH_TOKEN
ENV POETRY_HTTP_BASIC_BREW_USERNAME=aws \
    POETRY_HTTP_BASIC_BREW_PASSWORD=${CODEARTIFACT_AUTH_TOKEN}
RUN poetry config virtualenvs.create false\
    && poetry install --no-interaction --no-ansi

# install dockerize
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY . .
COPY ./scripts/docker/celery-entrypoint.sh ./celery-entrypoint.sh
COPY ./scripts/docker/django-entrypoint.sh ./django-entrypoint.sh
COPY ./scripts/docker/entrypoint.sh ./entrypoint.sh

RUN chmod 755 './celery-entrypoint.sh' \
  && chmod 755 './django-entrypoint.sh' \
  && chmod 755 './entrypoint.sh'

RUN wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
  && chmod 755 /usr/local/bin/tini && tini --version

EXPOSE 8000
