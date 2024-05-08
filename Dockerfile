FROM python:3.11-slim

ENV PYTHONBUFFERED 1

WORKDIR /BizIntelliScan

COPY . /BizIntelliScan

RUN pip install -r requirments.txt

RUN python manage.py makemigrations authUser main task_calendar view_sheet

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "127.0.0.1:8888", "settings.wsgi"]

EXPOSE 8888
