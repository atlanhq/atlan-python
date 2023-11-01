FROM python:3.9.16-slim-buster

ARG VERSION

WORKDIR /app

RUN pip3 install requests>=2.24 pydantic==1.10.12 jinja2==3.1.2 networkx==3.1 tenacity==8.2.3
RUN pip3 install pyatlan==${VERSION}

CMD ["python"]
