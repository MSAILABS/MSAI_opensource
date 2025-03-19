FROM python:3.11-slim AS agents

WORKDIR /agents

# Copy requirements file first to enable caching for dependency installation
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

COPY . .

# Expose port 8000
EXPOSE 8000

CMD ["python", "./main.py"]
