import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from biz.agent import run

load_dotenv('.env')
load_dotenv('.env.local', override=True)

app = Flask(__name__)

used_ai_model = os.getenv('USE_AI_MODEL')
if used_ai_model is None:
    raise EnvironmentError("USE_AI_MODEL environment variable not set.")
if used_ai_model not in ['gemini', 'openai']:
    raise ValueError(f"USE_AI_MODEL Setting Errors: {used_ai_model}, only support 'gemini' or 'openai' in current version.")

@app.route('/suggestion', methods=['GET'])
def suggest_sonarqube_issues():
    project_key = request.args.get('project_key')
    merge_request_iid = request.args.get('merge_request_iid')

    if not project_key or not merge_request_iid:
        return jsonify({"error": "Both project_key and merge_request_iid are required."}), 400

    result = run(used_ai_model, project_key, merge_request_iid)
    return jsonify({"message": "AI suggestion for SonarQube issues completed!", "data": result}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
