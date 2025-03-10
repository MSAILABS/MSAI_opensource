FROM python:3.11-slim AS backend

WORKDIR /backend

COPY . .

# Create and activate a virtual environment
RUN /bin/bash -c "pip install -r requirements.txt"

CMD ["python", "./main.py"]
