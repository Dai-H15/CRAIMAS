FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

WORKDIR /CRAIMAS

COPY . /CRAIMAS

RUN pip install -r requirements.txt

RUN python install_linux.py

RUN python manage.py collectstatic --noinput

EXPOSE 8000