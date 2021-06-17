FROM python:3.8-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y debconf fonts-noto-extra postgresql-client xauth wkhtmltopdf locales jpegoptim && \
    apt-get install -y gcc && \
    python3 -m pip install requests psycopg2 beautifulsoup4 boto3 firebase-admin pytz --no-cache-dir && \
    apt-get remove -y gcc && \
    rm -rf /var/lib/apt/lists/*

RUN echo "es_AR UTF-8" > /etc/locale.gen && \
    locale-gen

RUN fc-cache -fv
COPY bluelytics-mobile-firebase-adminsdk.json /
COPY ./src /app

ENV GOOGLE_APPLICATION_CREDENTIALS="/bluelytics-mobile-firebase-adminsdk.json"

ENTRYPOINT /app/entrypoint.sh