FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && mkdir -p logs

COPY . .

# по умолчанию — запускаем бота
CMD ["python", "bot.py"]