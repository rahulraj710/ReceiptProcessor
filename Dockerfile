FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files to container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run Django's development server when container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
