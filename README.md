# awesome-react-flask-docker
Hackathon template with a React frontend and Flask backend. Docker containers for easy deployment.

Libraries already included:
```bash
tailwindcss
react-router-dom
polished
```

# Running

## In Development

You need `Node.js` (to use `npm`) and `Python` with the required dependencies. On MacOS:
```bash
# For the React package manager
brew install node
# Python dependencies
conda create -n backend Python=3.9
conda activate backend
conda install --file backend-react-client/requirements.txt
```

Install [Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) and [docker-compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository).

Running the app:

```bash
# Run the backend before the frontend.
cd backend-flask-server
flask run

cd ../frontend-react-client
npm run start
```

> The backend listens to port `4000` (because MacOS hijacks the default). If you want to change this, you need to modify the following files:
>- `backend-flask-server/.flaskenv`
>- `Dockerfile.backend`
>- `frontend-react-client/deployment/nginx.default.conf`
>- `frontend-react-client/package.json`
> 
> The frontend listens to default port `3000`.

## Deployment

Using a Gunicorn server for the Python project, and nginx as a reverse proxy in front of it. All commands are run from the root directory.

### Building the Docker images together with docker-compose

```bash
docker compose up
```

or `docker-compose up` on older versions. Use `docker compose up -d --no-deps --build` to rebuild.

### Building the Docker images separately for testing
```bash
# backend
docker build -f Dockerfile.backend -t app-backend .
# frontend
docker build -f Dockerfile.frontend -t app-frontend .
```
Running the backend Docker image for testing: `docker run --rm -p 4000:4000 app-backend`. Then navigate to `localhost:4000/`. Running the frontend image will result in a failure from nginx, which is not going to recognize the http://api:5000 proxy URL.

### Deploying on GCP

- Choose a VM type, e.g. `e2-medium`.
- Choose a boot disk. I like `Ubuntu 20.04 LTS`.
- Enable HTTP and HTTPS traffic.
- Add an SSH key
- Create the VM.
- Go to `Network interfaces` > Click on `Network details` > `VPC Network` > `Firewall` > `CREATE FIREWALL RULE`
    - Apply it to the VM: Under `Targets` select `Specified target tags` and enter `<SOME_TAG_NAME>`
        - Or just apply it to all VMs.
    - Set `Source IPv4 Ranges` to `0.0.0.0/0`
    - In `Protocols and Ports` check `TCP` and enter `3000` (or whatever port to expose)
    - Create the rule and apply the tag `<SOME_TAG_NAME>` to the VM instance.

# References

Based on the [React + Flask + Docker tutorial](https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project) from Miguel Grinberg. [Part2](https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project), [Part3](https://blog.miguelgrinberg.com/post/how-to-deploy-a-react-router-flask-application), [Part4](https://blog.miguelgrinberg.com/post/how-to-dockerize-a-react-flask-project).

Set up tailwindcss according to these [instructions](https://tailwindcss.com/docs/guides/create-react-app).


# Other Hackathon Stuff

- [Color Generator](https://coolors.co)
- [Perfect Devpost Template](https://devpost.com/software/example-template-submission)
- [6-3-5 Method Miro Board](https://miro.com/miroverse/635-method-6-people-3-ideas-5-minutes/)
