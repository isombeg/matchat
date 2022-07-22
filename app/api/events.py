from flask import Flask, Blueprint, Response, request
from app.utils.response_dispatcher import response_dispatcher
from app.utils.constants import BLOCK_ACTIONS_DISPATCHER
from app.api.home import get_profile_handler

events_bp = Blueprint('events', __name__)

@events_bp.post('/events')
def events_handler():
    print(f"events_handler: handling request. request = {request}")
    return response_dispatcher(request, events_router)

def events_router(request) -> Response:
    print("event_router: routing...")

    if "event" in request.json and request.json["event"]["type"] == "app_home_opened":
        print("app_home_opened event received")
        return get_profile_handler(request)
        
    return Response(status=200)