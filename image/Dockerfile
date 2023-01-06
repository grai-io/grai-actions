FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY src /src
COPY entrypoints /entrypoints/

RUN pip3 install --no-cache-dir --upgrade pip \
 && pip3 install --no-cache-dir -r /src/requirements.txt


ENTRYPOINT ["/entrypoints/entrypoint.sh"]
