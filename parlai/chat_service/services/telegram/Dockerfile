FROM python:3-alpine

RUN apk add --update --no-cache --virtual .build-deps gcc musl-dev libffi-dev libressl-dev  \
    && pip install --no-cache-dir python-telegram-bot websocket-client==0.56.0 \
    && apk del .build-deps

COPY client.py app/client.py

CMD [ "python", "/app/client.py" ]
