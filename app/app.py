import profile
from flask import Flask, request, Response
from app.api.profile import post_profile_handler, profile_view_handler
from app.api.match import match_bp
from app.api.home import get_profile_handler
from app.utils.constants import ACTION_ID_EDIT_PROFILE

app = Flask(__name__)

app.register_blueprint(match_bp)

@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/")
def post_handler():
    print(f"post_handler: handling request. request = {request}")

    if not request.data:
        print("post_handler: received empty request")
        return Response(status=200)

    print(f"post_handler: slack payload: {request.json}")
    if "challenge" in request.json:
        print("post_handler: resolving challenge")
        return request.json["challenge"]
    
    return router(request)

def router(request) -> Response:
    print("router: Routing")

    if "event" in request.json and request.json["event"]["type"] == "app_home_opened":
        print("app_home_opened event received")
        return get_profile_handler(request)
        
    elif "type" in request.json and request.json["type"] == "block_actions":
        print("block_actions event received")
        action_id = request.json["actions"][0]["action_id"]
        return BLOCK_ACTIONS_DISPATCHER[action_id](request)
        
    # elif event_type == "view_submission":
    #     return

    return Response(status=200)

BLOCK_ACTIONS_DISPATCHER = {
    ACTION_ID_EDIT_PROFILE: profile_view_handler
}
