# 🦖 Logzilla - hackaTUM23 Rohde & Schwarz Challenge
> "A solution that will eat up your logs like Godzilla, and will then talk to you about it"

![logo192](https://github.com/HackaTUM-2023-MACP/Logzilla/assets/45896065/188bf01e-f044-4c5a-81ce-f65a9bc110bf)

Submission for the HackaTUM 2023 challenge "Rohde & Schwarz: Summarizing and Chatting with log files" | [Devpost](https://devpost.com/software/logzilla?ref_content=my-projects-tab&ref_feature=my_projects)

# How to Use it:

1. **Upload**: Upload your log file.
2. **Summarize**: Receive a brief summary of the log file to quickly grasp its key points.
3. **Interact**: Engage in a conversation with the chatbot to explore specific log entries and refine the summary based on your interests.
4. **Dynamic Updates**: The system continuously adapts the summary based on your queries and conversation history, ensuring a personalized and efficient user experience.

## Watch the Demo on YouTube
[![Watch the Demo on YouTube.](https://github.com/HackaTUM-2023-MACP/Logzilla/assets/45896065/14868fbf-a0c2-4b8f-afa9-ae9b31892ab6)](https://youtu.be/5oBkJUfh7PI?si=FYCHrDTPwncpWO9M)

## How it works:

The AI-powered system in the backend parses the logs, filters accordingly, and keeps track of a database generated from the initial file. The system predicts queries in parallel to the chat to retrieve the most relevant entries from the database (which correspond to log rows) to then present them to the user and incorporate to the current summary iteratively.

![Screenshot 2023-11-20 at 11 45 01](https://github.com/HackaTUM-2023-MACP/Logzilla/assets/45896065/6a62a3fc-ba37-4e97-8172-f1d86af78b89)


# 🏃Running

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
DANGEROUSLY_DISABLE_HOST_CHECK=true npm run start
```

> The backend listens to port `4000` (because MacOS hijacks the default). If you want to change this, you need to modify the following files:
>- `backend-flask-server/.flaskenv`
>- `Dockerfile.backend`
>- `frontend-react-client/deployment/nginx.default.conf`
>- `frontend-react-client/package.json`
> 
> The frontend listens to default port `3000`.


- [Color Generator](https://coolors.co)
- [Perfect Devpost Template](https://devpost.com/software/example-template-submission)
- [6-3-5 Method Miro Board](https://miro.com/miroverse/635-method-6-people-3-ideas-5-minutes/)
