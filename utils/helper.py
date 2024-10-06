def extract_sonarqube_issue_message(messages: list[dict]) -> dict:
    if messages is None:
        return {"message": ""}

    message = ""
    for item in messages:
        context = item.get('textRange')
        start_line = context.get('startLine')
        end_line = context.get('endLine')
        message += f"""Lines between {start_line} and {end_line} exist SonarQube Error: {item.get('message')}"""

    return [{"message": message}]
