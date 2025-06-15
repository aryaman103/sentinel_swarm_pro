FROM python:3.11-slim

# Install Poetry via the official install script
RUN pip install --upgrade pip && pip install poetry

WORKDIR /app
COPY . .

# Install dependencies
RUN poetry install --no-root

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
