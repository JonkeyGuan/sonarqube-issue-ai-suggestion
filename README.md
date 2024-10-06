# SonarQube Issue AI Suggestion

SonarQube Issue AI Suggestion is using AI models to automate Sonar Issue fixing suggestion.

## Implementation ideas

Get issue by gitlab merge request from SonarQube, invoke AI models for Issue fixing, add AI suggestion to gitlab MR comment.

## Thanks

This project is inspired by Alessandro-Pang's https://github.com/Alessandro-Pang/sonar-bugfix-ai

## Note

This project to demonstrate how to use AI automation to fix Sonar Issues. Please do not use it in a production environment directly.

## Dependencies

- Python 3.10+

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Modify the configuration items in `.env` file. Please note that you will need to apply for your AI ​​model token.

By default, the Google AI `gemini` model is used. If you want to use OpenAI `ChatGPT` model, please modify `USE_AI_MODEL` in `.env` file to `openai`.

```dotenv
USE_AI_MODEL=gemini

GEMINI_AI_MODEL=gemini-pro
GOOGLE_API_KEY=your_api_key

OPENAI_API_URL=https://api.openai.com/
OPENAI_AI_MODEL=gpt-4-turbo
OPENAI_API_KEY=your_api_key

SONARQUBE_URL=http://localhost:9000
SONARQUBE_TOKEN=your_token
SONARQUBE_TLS_VERIFY=False

GITLAB_URL=http://localhost:9001
GITLAB_TOKEN=your_token
GITLAB_TLS_VERIFY=False
```

## Usage

```bash
gunicorn -w 4 -b 0.0.0.0:8080 app:app

curl http://localhost:8080/suggestion?project_key=<project_key>&merge_request_iid=<merge_request_iid>

```
