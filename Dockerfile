# Base image
FROM python:3.11.0-alpine

# Set the working directory
WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copy only the necessary files to the container
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Expose the port that the application will listen on
EXPOSE 8000

# Start the application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
