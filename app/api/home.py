from flask import request, Blueprint, Response, json
from os import environ
import requests
from app.models.profile import Profile
from pymongo import MongoClient
from app.block_kits.home import *
from app.utils.constants import ATLAS_CONNECTION_STR, SLACK_API_URL, API_VIEWS_PUBLISH, SLACK_BOT_TOKEN
from json import dumps
from threading import Thread

mongo_client = MongoClient(ATLAS_CONNECTION_STR)

def get_profile_handler(request):
    json_body = request.json
    slack_id = json_body["event"]["user"]

    thread_send_home_view = Thread(
        target=send_home_view,
        kwargs={
            "slack_id": slack_id
        }
    )
    thread_send_home_view.start()

    return Response(status=200)

    

def send_home_view(slack_id):
    # extract user profile from coll
    profiles_coll = mongo_client.matchat.profiles
    profile_doc = profiles_coll.find_one({"slack_id": slack_id})

    response = None

    if profile_doc is None:
        print("get_profile_handler: user is not yet registed")
        response = requests.post(
            f"{SLACK_API_URL}{API_VIEWS_PUBLISH}",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json=uncreated_profile_home(slack_id)
        )
    
    else:
        print("send_home_view: user is registered")
        response = requests.post(
            f"{SLACK_API_URL}{API_VIEWS_PUBLISH}",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json=created_profile_home(
                Profile(
                    slack_id=slack_id,
                    name = profile_doc["name"],
                    is_intern = profile_doc["is_intern"],
                    team_id = profile_doc["team"],
                    prefers_interns = profile_doc["prefers"]["interns"],
                    prefers_ftes = profile_doc["prefers"]["ftes"],
                    is_active = profile_doc["is_active"],
                    opt_in = profile_doc["opt_in"],
                    met_with = profile_doc["met_with"]
                )
            )
        )

    print(f"send_home_view: request sent: {response.request.body}")
    print(f"send_home_view: response received: {response.text}")

    if response.status_code == 200:
        print("send_home_view: home tab publishing succesful")
    else:
        print("send_home_view: home tab publishing Unsuccesful")
    
    return