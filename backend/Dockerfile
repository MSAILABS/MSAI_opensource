FROM python:3.11-slim AS backend

WORKDIR /backend

# Copy requirements file first to enable caching for dependency installation
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./main.py"]
