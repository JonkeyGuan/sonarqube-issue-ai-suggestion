import importlib
import os

from adapter.sonarqube import fetch_issues_by_componnent_pr, get_raw_code, get_project_id_by_project_key
from adapter.gitlab import get_merge_reqeust_diff, comment_to_merge_request
from utils.helper import extract_sonarqube_issue_message

def run(ai_model: str, project_key: str, merge_request_iid: str) -> str:
    print("Start Loading SonarQube issue(s) ...")
    issues = fetch_issues_by_componnent_pr(project_key, merge_request_iid)
    print("Loaded, processing ...")

    ai_module = importlib.import_module(f'models.{ai_model}')
    run_ai = ai_module.run_ai

    index = 0
    total = len(issues)
    for componentKey in issues:
        index += 1
        print(f"\rCurrent progress {index}/{total} \n", end="", flush=True)
        component_issues = issues.get(componentKey)
        component = component_issues.get('component')
        project = get_project_id_by_project_key(project_key)
        diff = get_merge_reqeust_diff(project, merge_request_iid, component.get('path'))
        raw_code = get_raw_code(component.get('key'))
        if len(raw_code) == 0:
            continue

        message = extract_sonarqube_issue_message(component_issues.get('message_list'))
        ai_suggestion = run_ai(raw_code, diff, message)
        print(f"\ndiff code: ")
        print(f"{diff} ")
        
        print(f"ai suggestion:")
        print(f"\n{ai_suggestion}")

        comment_to_merge_request(project, merge_request_iid, ai_suggestion)

    return "done"
