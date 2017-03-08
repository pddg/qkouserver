FROM alpine:3.5

LABEL maintainer "pudding <pudding@mail.poyo.info>"

ENV DATA_DIR /data
ENV PRJ_PATH /srv/qkouserver
ENV SQLITE_PATH ${DATA_DIR}

RUN apk --update add gcc \
    g++ \
    python3 \
    python3-dev \
    libxml2 \
    libxml2-dev \
    libxslt \
    libxslt-dev && \
    echo "Asia/Tokyo" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    mkdir ${DATA_DIR} && \
    mkdir ${PRJ_PATH}

COPY . ${PRJ_PATH}

WORKDIR ${PRJ_PATH}

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "manage.py"]

CMD ["-h"]