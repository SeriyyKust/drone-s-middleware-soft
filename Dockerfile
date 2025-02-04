FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN mkdir /app
RUN mkdir /app/logs
WORKDIR /app


RUN apt-get update

COPY ./requirements.txt /app/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY ./. /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]