FROM python:3.8-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y debconf fonts-noto-extra postgresql-client xauth wkhtmltopdf locales && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get install -y gcc && \
    python3 -m pip install requests psycopg2 beautifulsoup4 boto3 --no-cache-dir && \
    apt-get remove -y gcc && \
    rm -rf /var/lib/apt/lists/*

RUN echo "es_AR UTF-8" > /etc/locale.gen && \
    locale-gen

RUN fc-cache -fv
COPY ./src /app

ENTRYPOINT /app/entrypoint.sh