#!/bin/bash

pip3 install grai-source-mssql

apt update && apt install -y unixodbc gnupg2
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

source /entrypoints/entrypoint.sh
