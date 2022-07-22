from threading import Thread
from flask import request, Blueprint, Response, json
from os import environ
import requests
from app.block_kits.profile import PROFILE_MODAL_DICT
from app.models.profile import Profile
from pymongo import MongoClient
from app.utils.constants import SLACK_BOT_TOKEN

SLACK_API_URL = environ.get("SLACK_API_URL")
ATLAS_CONNECTION_STR = environ.get("ATLAS_CONNECTION_STR")

mongo_client = MongoClient(ATLAS_CONNECTION_STR)

def post_profile_handler(request):
    json_body = request.json
    values = json_body["view"]["state"]["values"]
    
    profile = Profile(
        json_body["user"]["id"],
        json_body["user"]["name"],
        values["emp_type"]["static_select-action"]["value"] == "Intern",
        json_body["user"]["team_id"],
        "Interns" in values["preference"]["preference-multi_static_select-action"]["value"],
        "Full-time Employees" in values["preference"]["preference-multi_static_select-action"]["value"],
    )

    thread_update_profile = Thread(
        target=update_profile,
        kwargs={"profile": profile}
    )
    thread_update_profile.start()

    return Response(status=200)

# Handler when user updates profile, TODO: this
def update_profile(profile):
    profiles_coll = mongo_client.matchat.profiles
    profile_doc = profiles_coll.find_one(profile.slack_id)

    acknowledged = None
    
    if profile_doc is None:
        acknowledged = profiles_coll.insert_one(profile.getObjDict())
    else:
        acknowledged = profiles_coll.update_one(
            {"slack_id": profile.slack_id},
            profile.getProfileInfoDict()
        )

    print(f"updated profiles collections {acknowledged}")
    return


def profile_view_handler(request):
    json_body = request.json
    trigger_id = json_body["trigger_id"]

    thread_send_profile_form = Thread(
        target=send_profile_form,
        kwargs={
            "trigger_id": trigger_id
        }
    )
    thread_send_profile_form.start()
    
    return Response(status=200)

def send_profile_form(trigger_id):
    request_body = {
        "trigger_id": trigger_id,
        "view": PROFILE_MODAL_DICT,
    }

    print(f"send_profile_form: Sending profile edit modal to slack for trigger_id {trigger_id}")
    response = requests.post(
        f"{SLACK_API_URL}/api/views.open",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json=request_body
    )

    if response.status_code == 200:
        print("send_profile_form: Successfully sent modal")
        return
    
    print("send_profile_form: Unsuccessfully sent modal")
    return
