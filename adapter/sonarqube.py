import json
import math
import os
from typing import Any

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_project_id_by_project_key(project_key: str) -> str:
    params = {
        'project': project_key
    }
    response = _make_request('/alm_settings/get_binding', params)
    return response.json().get('repository', '') 

def get_raw_code(issue_key) -> str:
    params = {
        'key': issue_key  # Issue key
    }  
    response = _make_request('/sources/raw', params)
    return response.text

def fetch_issues_by_componnent_pr(component_key: str, pr_id: str) -> dict[str, Any]:
    print(f"Loading issue(s) ...")
    params = {
        'statuses': 'OPEN',
        'componentKeys': component_key,
        'pullRequest': pr_id
    }
    response = _make_request('/issues/search', params).json()

    issues = response.get('issues')
    components = response.get('components')
    result = []

    for issue in issues:
        text_range = issue.get('textRange')
        if text_range is None:
            continue
        component_id = issue.get('component')
        message = issue.get('message')
        component = _find_component_by_id(components, component_id)
        max_range = _extract_max_range(issue.get('flows'), text_range)
        result.append({"message": message, "text_range": max_range, "component": component})
    return _group_issue_by_component_id(result)

def _group_issue_by_component_id(issues: list[dict]) -> dict:
    components = {}
    for issue in issues:
        component = issue.get('component')
        component_id = component.get('key')

        if not components.get(component_id):
            components[component_id] = {"component": component, "message_list": []}

        cached_issue = components[component_id]
        cached_issue.get('message_list').append({
            "message": issue.get('message'),
            "textRange": issue.get('text_range')
        })
    return components

def _find_component_by_id(component_list: list, component_id: str) -> dict:
    for component in component_list:
        if component.get('key') == component_id:
            return component
    return {}

def _extract_max_range(flows: list[dict], parent_range) -> dict:
    flow_range = parent_range
    for flow in flows:
        for location in flow.get('locations'):
            text_range = location.get('textRange')
            if text_range is None:
                continue
            startLine = text_range.get('startLine')
            endLine = text_range.get('endLine')
            flow_range['startLine'] = startLine if startLine < flow_range['startLine'] else flow_range['startLine']
            flow_range['endLine'] = endLine if endLine > flow_range['endLine'] else flow_range['endLine']
    return flow_range

def _make_request(api_endpoint: str, params: dict) -> dict:
    sonarqube_url = os.getenv('SONARQUBE_URL')
    api_token = os.getenv('SONARQUBE_TOKEN')
    auth = requests.auth.HTTPBasicAuth(api_token, '')
    tls_verify = os.getenv('SONARQUBE_TLS_VERIFY', 'True').lower() == 'true'
    
    response = requests.get(f'{sonarqube_url}/api{api_endpoint}', auth=auth, params=params, verify=tls_verify)
    if response.ok:
        return response
    elif response.status_code == 404:
        print("SonarQube 404 Not Found")
    elif response.status_code == 401:
        print("SonarQube Authorization Failed")
    elif response.status_code == 403:
        print("SonarQube No Permission to Access")
    elif response.status_code == 500:
        print("SonarQube Server Error")
    else:
        print("Error:", response.status_code)
    return {}
