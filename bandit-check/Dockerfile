# Copyright 2020 Cognite AS
FROM python:alpine3.12

COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN pip install bandit

ENTRYPOINT ["/entrypoint.sh"]
