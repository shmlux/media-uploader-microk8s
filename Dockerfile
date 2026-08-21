FROM python:3.11-slim

WORKDIR /app

# Copy application dependencies and source code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose HTTP port 80
EXPOSE 80

# Create directory for pesistent uploads
RUN mkdir -p /app/uploads

CMD ["python", "app.py"]

