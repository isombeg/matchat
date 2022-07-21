import profile
from flask import Flask
from app.api.profile import profile, profile_view
from app.api.match import match_bp
from app.api.home import home

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(profile_view)
app.register_blueprint(profile)
app.register_blueprint(match_bp)
app.register_blueprint(home)