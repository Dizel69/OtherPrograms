from flask import Flask, request, abort  
import requests  
  
app = Flask(__name__)  
  
PUSHGATEWAY_URL = "http://200.0.10.124:9091/metrics/job/gitlab_metrics"  
  
  
def escape(value):  
    """Экранирование допустимых спецсимволов для значений меток Prometheus"""  
    return str(value).translate(str.maketrans({  
        '"': r'\"',  
        '\\': r'\\',  
        '\n': r'\n'  
    }))  
  
  
@app.route('/webhook', methods=['POST'])  
def gitlab_webhook():  
    data = request.json  
    # Определяем тип события: push, build (job) или pipeline  
    event = data.get("object_kind")  
    if event is None:  
        header_event = request.headers.get("X-Gitlab-Event", "").lower()  
        if "push" in header_event:  
            event = "push"  
        else:  
            abort(400, "Cannot determine event type")  
  
    # Попробуем получить значение kind из JSON, если его нет – используем event  
    kind = escape(data.get("kind", event))  
  
    if event == "push":  
        # Для push-события  
        project_obj = data.get("project", {})  
        # Используем path_with_namespace, приводим к нижнему регистру  
        project = escape(project_obj.get("path_with_namespace", "unknown").lower())  
        avatar_url = escape(project_obj.get("avatar_url", "unknown"))  
        branch = escape(data.get("ref", "unknown").split("/")[-1])  
        user = escape(data.get("user_name", "unknown"))  
        user_id = data.get("user_id", "unknown")  
        user_username = escape(data.get("user_username", "unknown"))  
        commits = data.get("commits", [])  
        commit_message = escape(commits[0].get("message", "")) if commits else ""  
        value = data.get("total_commits_count", 1)  
    elif event == "build":  # Job Event  
        project_obj = data.get("project", {})  
        project = escape(project_obj.get("path_with_namespace", "unknown").lower())  
        avatar_url = escape(project_obj.get("avatar_url", "unknown"))  
        branch = escape(data.get("ref", "unknown"))  
        user_obj = data.get("user", {})  
        user = escape(user_obj.get("name", "unknown"))  
        user_id = user_obj.get("id", "unknown")  
        user_username = escape(user_obj.get("username", "unknown"))  
        commit_message = escape(data.get("commit", {}).get("message", ""))  
        value = 1  
    elif event == "pipeline":  
        project_obj = data.get("project", {})  
        project = escape(project_obj.get("path_with_namespace", "unknown").lower())  
        avatar_url = escape(project_obj.get("avatar_url", "unknown"))  
        branch = escape(data.get("object_attributes", {}).get("ref", "unknown"))  
        user_obj = data.get("user", {})  
        user = escape(user_obj.get("name", "unknown"))  
        user_id = user_obj.get("id", "unknown")  
        user_username = escape(user_obj.get("username", "unknown"))  
        commit_message = escape(data.get("commit", {}).get("message", ""))  
        value = 1  
    else:  
        abort(400, f"Unsupported event type: {event}")  
  
    # Формируем строку метрики с метками, включая новый лейбл kind  
    labels = (  
        f'event="{event}", '  
        f'kind="{kind}", '  
        f'project="{project}", '  
        f'branch="{branch}", '  
        f'user="{user}", '  
        f'user_id="{user_id}", '  
        f'user_username="{user_username}", '  
        f'avatar_url="{avatar_url}", '  
        f'commit_message="{commit_message}"'  
    )  
    metric_line = f'gitlab_event_info{{{labels}}} {value}\n'  
  
    app.logger.info(f"Sending metrics:\n{metric_line}")  
    try:  
        response = requests.post(  
            url=PUSHGATEWAY_URL,  
            data=metric_line,  
            headers={'Content-Type': 'text/plain; version=0.0.4'},  
            timeout=5  
        )  
        response.raise_for_status()  
        return "OK", 200  
    except Exception as e:  
        app.logger.error(f"Error pushing to Pushgateway: {str(e)}", exc_info=True)  
        abort(500, "Failed to push metrics")  
  
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5001, debug=True)