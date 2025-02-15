# Gotify to PushDeer Forwarder

This project listens to messages from Gotify and forwards them to PushDeer.

## Prerequisites

- Docker
- Python 3.9+

## How to Use

1. Clone the repository:
   ```bash
   git clone https://git.geekmt.com/sam/gotify-to-pushdeer.git

 2. Build the Docker image:

```bash
docker build -t gotify-to-pushdeer .
```
3. Run the Docker container:

```bash
docker run -d --name gotify-pushdeer-container gotify-to-pushdeer
```


4. GitHub Actions
This project uses GitHub Actions to automatically build and push Docker images to Docker Hub.

License
MIT