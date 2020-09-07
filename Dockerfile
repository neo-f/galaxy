FROM tiangolo/uvicorn-gunicorn:python3.8-slim

ENV PYTHONUNBUFFERED 1
ENV TZ Asia/Shanghai

COPY requirements/production.txt /tmp/requirements.txt

RUN set -ex \
    && sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list \
    && sed -i "s/security.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r /tmp/requirements.txt \
    && apt-get clean autoclean \
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache /var/lib/apt/lists/* /var/lib/{apt,dpkg,cache,log}/

COPY . /app
WORKDIR /app
