import profile
from flask import Flask, request, Response
from app.api.profile import profile, profile_view
from app.api.match import match_bp
from app.api.home import get_profile_handler

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/")
def post_handler():
    if "challenge" in request.json:
        return request.json["challenge"]
    
    return router(request)

def router(request) -> Response:
    print(f"Slack Payload: {request.json}")
    event_type = request.json["event"]["type"]
    if event_type == "app_home_opened":
        print("app_home_opened event received")
        return get_profile_handler(request)
    elif event_type == "block_actions":
        return {
        }[request.json["actions"]]
    elif event_type == "view_submission":
        return
