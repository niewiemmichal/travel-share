FROM python:3.8-alpine

RUN apk add --no-cache postgresql-dev build-base libffi-dev

WORKDIR /app
COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["gunicorn", "travelshare.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
