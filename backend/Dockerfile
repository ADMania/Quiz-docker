FROM python:3.11-alpine

WORKDIR /app

# системные зависимости
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# собираем статику
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "quiz.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]