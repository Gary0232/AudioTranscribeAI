# AudioTranscribeAI

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

#### Go to the frontend folder
```bash
cd frontend/AudioTranscribeAI
```

The frontend is built with node.js and vue.js.

To start the server, you need to install the [node.js](https://nodejs.org/en/download) and yarn package manager.

```bash
npm install --global yarn
```

#### Install the requirements
```bash
yarn
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

## Build the frontend application
```bash
yarn build
```
