FROM python:3.9-bookworm


RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64
RUN chmod +x /usr/local/bin/dumb-init

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /app

ADD dummy /app/dummy

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
