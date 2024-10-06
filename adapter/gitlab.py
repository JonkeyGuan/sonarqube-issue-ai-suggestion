import json
import math
import os
from typing import Any

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_merge_reqeust_diff(project_id: str, merge_request_iid: str, file_path: str) -> str:
    url = os.getenv('GITLAB_URL')
    token = os.getenv('GITLAB_TOKEN')

    # Prepare authentication for the request
    auth = requests.auth.HTTPBasicAuth(token, '')
    
    tls_verify = os.getenv('GITLAB_TLS_VERIFY', 'True').lower() == 'true'
    
    api_endpoint = f"{url}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/changes"

    response = requests.get(api_endpoint, auth=auth, verify=tls_verify)

    if response.status_code == 200:
        changes = response.json().get('changes', [])
        for change in changes:
            if change['new_path'] == file_path:
                return change['diff']  # 返回特定文件的diff信息
        
        return {f"message: File not found in the merge request: {file_path}"}
    else:
        print(f"Failed to fetch: {response.status_code}, {response.text}")
