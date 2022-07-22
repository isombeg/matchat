from app.models.profile import Profile
from app.utils.constants import SLACK_USER_ID, SLACK_BOT_TOKEN, ACTION_ID_EDIT_PROFILE, BLOCK_ID_CREATE_PROFILE


def created_profile_home(profile : Profile):
    return {
        "token": SLACK_BOT_TOKEN,
        "user_id": SLACK_USER_ID,
        "view": {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Profile",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Name*\n{profile.name}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Status*\n{'Intern' if profile.is_intern else 'Full-time Employee'}"
                    }
                },
                {
                    "type": "section",
                    "block_id": "edit_profile",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Preference*\n{'Interns and Full-time Employees' if len(profile.prefers) == 2 else profile.prefers[0]}"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Edit Profile",
                            "emoji": True
                        },
                        "value": "click_me_123",
                        "action_id": "button-action"
                    }
                }
            ]
        }
}
    

def uncreated_profile_home(slack_id): 
    return {
        "token": SLACK_BOT_TOKEN,
        "user_id": slack_id,
        "view": {
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Click Me"
                },
                "value": "click_me_123",
                "action_id": "button"
                } 
        }
    }
