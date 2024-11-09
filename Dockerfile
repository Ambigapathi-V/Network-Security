# Use Python 3.10 slim image as a base
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the current directory into the /app directory in the container
COPY . /app

# Install system dependencies needed by your application
RUN apt-get update && apt-get install -y gcc musl-dev libpq-dev

# Install Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the command to run the Streamlit app when the container starts
CMD ["streamlit", "run", "app.py"]
