from os import environ

PORT = int(environ.get("PORT", 5000))
ATLAS_CONNECTION_STR = environ.get("ATLAS_CONNECTION_STR")
SLACK_API_URL = environ.get("SLACK_API_URL")
SLACK_USER_ID = environ.get("SLACK_USER_ID")
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")

API_VIEWS_PUBLISH = "/api/views.publish"

BLOCK_ID_CREATE_PROFILE = "profile-editProfile"
BLOCK_ACTIONS_DISPATCHER = True
ACTION_ID_EDIT_PROFILE = "profile-editProfile"
