from dotenv import load_dotenv
load_dotenv()

import os

from flask import Flask, json

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

SECRET = os.getenv("SECRET")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
api_key = os.getenv("TWILIO_API_KEY")
api_secret = os.getenv("TWILIO_API_SECRET")

app = Flask(__name__)

@app.route('/grant/<identity>')
def get_grant(identity):
    """A stupid endpoint to grant access_tokens
    """
    if not identity:
        response = app.response_class(
            response=json.dumps({  }),
            status=400,
            mimetype='application/json'
        )
        return response

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a Video grant and add to token
    video_grant = VideoGrant()
    token.add_grant(video_grant)

    # Return token info as JSON
    jwt = token.to_jwt()

    response = app.response_class(
        response=json.dumps({ 'token': jwt.decode("utf-8") }),
        status=200,
        mimetype='application/json'
    )
    return response