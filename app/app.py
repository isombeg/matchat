from flask import Flask
from app.api.match import match_bp
from app.api.actions import actions_bp
from app.api.events import events_bp

app = Flask(__name__)

app.register_blueprint(match_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(events_bp)

@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"
