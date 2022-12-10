FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

COPY entrypoint.sh /app/entrypoint.sh

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "store.wsgi:application", "--bind", "0:7000" ]