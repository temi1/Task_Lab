FROM python:3.7

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

COPY ./log /app

COPY ./words /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]