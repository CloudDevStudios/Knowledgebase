# Start from an official Python runtime as a parent image
FROM python:3.9-slim
# Start from an official Python runtime as a parent image
FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
# Install system dependencies
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8000
# Expose port
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Add these lines before the CMD
ENV PINECONE_API_KEY=${PINECONE_API_KEY}
ENV PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT}