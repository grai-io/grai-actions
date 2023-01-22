FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY grai-actions /grai-actions
COPY entrypoints /entrypoints

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir /grai-actions


ENTRYPOINT ["/entrypoints/entrypoint.sh"]
