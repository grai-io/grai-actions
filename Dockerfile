FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY src /src

RUN pip3 install --no-cache-dir --upgrade pip \
 && pip3 install --no-cache-dir -r /src/requirements.txt


# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONBUFFERED=1 \
#     PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["/src/entrypoint.sh"]
