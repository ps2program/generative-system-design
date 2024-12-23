
# Docker Guide for xSytemsAI

This guide provides instructions for building and running the `xsystemsai` Docker container, both with standard Docker commands and using Docker Compose.

## Building and Running Docker Container

### Building the Docker Image

First, build the Docker image named `xsystemsai` using the following command:

```bash
docker build -t xsystemsai .
```

### Running the Docker Container

After building the image, you can run the Docker container and map port 5000 on your local machine to port 5000 inside the container:

```bash
docker run -p 5050:5050 xsystemsai
```


# Alternate Method using Docker Compose - best approach

### Building the Docker Image using Docker Compose
Make sure to create .env file first with all env variables required

### Building the Docker Image using Docker Compose

To build and run your application using Docker Compose, use the following command:

```bash
docker-compose up --build
```

### Stopping the Containers

To stop and remove the containers created by Docker Compose, run:

```bash
docker-compose down
```
