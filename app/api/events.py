from flask import Flask, Blueprint, Response, request
from app.utils.response_dispatcher import response_dispatcher
from app.utils.constants import BLOCK_ACTIONS_DISPATCHER
from app.api.home import get_profile_handler
from app.api.profile import member_joined_channel_handler

events_bp = Blueprint('events', __name__)

@events_bp.post('/events')
def events_handler():
    print(f"events_handler: handling request. request = {request}")
    return response_dispatcher(request, events_router)

def events_router(request) -> Response:
    print("event_router: routing...")

    if "event" in request.json:
        event_type = request.json["event"]["type"]
        
        if event_type == "app_home_opened":
            print("events_router: app_home_opened event received")
            return get_profile_handler(request)

        elif event_type == "member_joined_channel":
            print("events_router: member_joined_channel event received")
            return member_joined_channel_handler(request)
        
    return Response(status=200)