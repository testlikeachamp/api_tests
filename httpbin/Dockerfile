FROM python:3-alpine

ENV WEB_CONCURRENCY=4


RUN apk add -U ca-certificates libffi libstdc++ &&\
    apk add --no-cache --virtual build-deps build-base libffi-dev && \
    # Pip
    pip install --no-cache-dir gunicorn httpbin && \
    # Cleaning up
    apk del --purge build-deps && \
    rm -rf /var/cache/apk/*

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "httpbin:app"]
