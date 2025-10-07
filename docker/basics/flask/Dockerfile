FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application package contents (so app/app.py becomes /app/app.py)
COPY app/ .

EXPOSE 5000

CMD ["python","app.py"]