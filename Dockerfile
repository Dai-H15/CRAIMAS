FROM python:3.11-slim

ENV PYTHONBUFFERED 1

WORKDIR /BizIntelliScan

COPY . /BizIntelliScan

RUN pip install -r requirments.txt

RUN python manage.py makemigrations authUser main task_calendar view_sheet

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:9999"]

EXPOSE 9999