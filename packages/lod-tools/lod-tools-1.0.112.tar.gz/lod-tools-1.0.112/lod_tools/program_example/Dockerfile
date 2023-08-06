

# base this Image on python 3
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# install the required libraries
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["python", "app.py"]
