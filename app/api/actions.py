from flask import Blueprint, Response, request
from app.utils.response_dispatcher import response_dispatcher
from app.utils.constants import ACTION_ID_EDIT_PROFILE 
from app.api.profile import profile_view_handler

actions_bp = Blueprint('actions', __name__)

@actions_bp.post('/actions')
def actions_handler():
    print(f"actions_handler: handling request. request = {request}")
    return response_dispatcher(request, actions_router)

def actions_router(request) -> Response:
    print("actions_router: routing...")

    if "type" in request.json and request.json["type"] == "block_actions":
        print("block_actions event received")
        return block_actions_dispatch(request)

    return Response(status=200)
    
def block_actions_dispatch(request):
    action_id = request.json["actions"][0]["action_id"]
    return {
        ACTION_ID_EDIT_PROFILE: profile_view_handler
    }[action_id](request)