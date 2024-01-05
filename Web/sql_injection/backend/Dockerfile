# Use the official Ubuntu 18.04 LTS as a base image
FROM ubuntu:18.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install Python 3 and pip
RUN apt-get update -y \
  && apt-get install -y python3-pip \
  && apt-get clean \
  && rm -rf /var/lib/apti/lists/*

# Install Flask, specifying the version to ensure reproducibility
RUN pip3 install Flask==1.0.2
RUN pip3 install flask-cors

# Copy the Python server script and the database file into the container
COPY server.py /
COPY database.sqlite /

# Set the working directory to the root (not strictly necessary here, as this is the default)
WORKDIR /

# Expose port 5000 for the Flask server
EXPOSE 5000

# Run the server.py script using Python 3 when the container launches
CMD ["python3", "server.py"]
