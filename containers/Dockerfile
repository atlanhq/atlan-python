FROM python:3.9.16-slim-buster

ARG VERSION

WORKDIR /app

COPY base /app/

RUN pip3 install pyatlan==${VERSION}

CMD ["python"]
