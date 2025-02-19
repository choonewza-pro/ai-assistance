# Docker compose

- docker-compose up -d
- docker-compose down
- docker-compose logs -f

# Dockerfile-OK-OLD
## Build
docker build -t my-jupyter .

## Run InteractiveE
docker run -p 8888:8888 my-jupyter

## Run Background
docker run -d -p 8888:8888 my-jupyter

## Run on server on internet
docker run -d -p 8888:8888 my-jupyter jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token='' --NotebookApp.allow_remote_access=True

Open your web browser and go to [http://localhost:8888] [http://122.155.209.179:8888] [http://122.155.209.179:8888/tree?]

xx