# Setup

## Requirements

| Tool    | Version |
|-------- |---------|
| Python  | 3.12    |
| Node    | 26      |


## Setup local LLM

Install Ollama: https://ollama.com/download

Download Qwen model:
```sh
ollama pull qwen3.5:2b
```

## Setup API

Setup Python virtual env

```sh
python -m venv venv
. ./venv/bin/activate
```

Install python dependencies

```sh
pip install -e '.[dev,test]'
```

## Setup web app

Install web app dependencies

```
npm --prefix app i
```

# Run

## Start Ollama server

```sh
ollama serve
```

Verify `qwen3.5:2` model is available: http://localhost:11434/api/tags

## Start API

```sh
fastapi dev api/main.py
```

Verify API is running: http://localhost:8000/health

## Start web app

```sh
npm --prefix app start
```

Open web app: http://localhost:4200

# Run tests

## Run API tests

```sh
tox
```
