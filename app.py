from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = "PASTE_YOUR_CLIENT_ID"
CLIENT_SECRET = "PASTE_YOUR_CLIENT_SECRET"
REDIRECT_URI = "https://verify-bot-production.up.railway.app/callback"

@app.route("/")
def home():
    return '<a href="/login">Login with Discord</a>'

@app.route("/login")
def login():
    url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify"
    )
    return redirect(url)

@app.route("/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": "1487522795113156769",
        "client_secret": "zPDmxrScuQXF24tlwwkcEENMs6ec_D4R",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    )

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    user_json = user_response.json()
    username = user_json.get("username", "Unknown")

    return f"Logged in as {username}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
