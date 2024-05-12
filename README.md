# AudioTranscribeAI

![Vue3](https://img.shields.io/badge/Vue-3.4.0-brightgreen)
![Vuetify3](https://img.shields.io/badge/Vuetify-3.5.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Node.js](https://img.shields.io/badge/Node.js-18.x-brightgreen)
![Yarn](https://img.shields.io/badge/Yarn-1.22.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.3-blue)
![sqlite3](https://img.shields.io/badge/sqlite-3-blue)

## Installation

This project is working with [Python 3.8.8+](https://www.python.org/), 
you should have it installed on your machine.

### Set up the backend

#### Install the requirements
```bash
pip install -r requirements.txt
```

### Set up the frontend

The frontend is inside the `frontend/AudioTranscribeAI` folder.

The application is built with node.js and vue.js.

So to start the server, you need to install the [node.js](https://nodejs.org/en/download) and yarn package manager.

```bash
npm install --global yarn
```

#### Install the requirements
```bash
yarn --cwd frontend/AudioTranscribeAI/  # if you are in the root directory
# or
cd frontend/AudioTranscribeAI 
yarn # if you are in the frontend/AudioTranscribeAI directory
```

## Run the application

Because we are using separate backend and frontend architecture, so we need to run both of them.

### Run the backend

```bash
python app.py
```
### Run the frontend

```bash
yarn --cwd frontend/AudioTranscribeAI/ dev # if you are in the root directory
# or
cd frontend/AudioTranscribeAI 
yarn dev # if you are in the frontend/AudioTranscribeAI directory
````

## Other commands for the frontend

## Build the release version of frontend application
```bash
yarn --cwd frontend/AudioTranscribeAI/ build # if you are in the root directory
# or
cd frontend/AudioTranscribeAI 
yarn build # if you are in the frontend/AudioTranscribeAI directory
```
