#!/bin/bash

# Set variables
POSTGRES_CONTAINER_NAME=${POSTGRES_CONTAINER_NAME:-logdb-postgres}
POSTGRES_PORT_MAPPING=${POSTGRES_PORT_MAPPING:-5432:5432}
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres

# Check if POSTGRES_PASSWORD is set
if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "ERROR: POSTGRES_PASSWORD must be set as an environment variable."
    exit 1
fi

# Check if PostgreSQL container exists
if [ "$(docker ps -aq -f name=$POSTGRES_CONTAINER_NAME)" ]; then
    echo -n "Container $POSTGRES_CONTAINER_NAME already exists. Do you want to recreate it? (y/n): "
    read response
    if [ "$response" != "y" ]; then
        echo "Container not recreated."
        exit 0
    fi

    # Stop and remove existing container
    docker stop $POSTGRES_CONTAINER_NAME
    docker rm $POSTGRES_CONTAINER_NAME
fi

# Run PostgreSQL instance with pgvector preinstalled
docker run --name $POSTGRES_CONTAINER_NAME -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -p $POSTGRES_PORT_MAPPING -d ankane/pgvector

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
until docker exec $POSTGRES_CONTAINER_NAME pg_isready -U $POSTGRES_USER; do
  sleep 1
done

# Run the Python script to initialize tables
python3 initialize_database.py --user $POSTGRES_USER --password $POSTGRES_PASSWORD --host $POSTGRES_HOST --port $POSTGRES_PORT

echo "Setup complete!"
