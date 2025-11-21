# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all needed scripts
COPY migration.py integrity.py auth_app.py create_user.py .

# Default command used by the "loader" service
CMD ["python", "migration.py"]
