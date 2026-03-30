from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = "1487522795113156769"
CLIENT_SECRET = "zPDmxrScuQXF24tlwwkcEENMs6ec_D4R"
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
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
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

    return f"""
<h2>Welcome {username}</h2>
<form action="/verify" method="post">
    <input type="text" name="insta" placeholder="Enter Instagram username" required>
    <button type="submit">Verify</button>
</form>
"""
@app.route("/verify", methods=["POST"])
def verify():
    insta_username = request.form.get("insta")

    return f"Checking Instagram for {insta_username}..."
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
