FROM python:3.11-slim AS agents

WORKDIR /agents

COPY . .

# Create and activate a virtual environment
RUN /bin/bash -c "pip install -r requirements.txt"

# Expose port 8000
EXPOSE 8000

CMD ["python", "./main.py"]
