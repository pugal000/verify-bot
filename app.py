from flask import Flask, redirect, request
import requests
import os

app = Flask(name)

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
user_id = user_json.get("id")  

return f"""

<h2>Welcome {username}</h2>  <form action="/verify" method="post">  
    <input type="hidden" name="user_id" value="{user_id}">  
    <input type="text" name="insta" placeholder="Enter Instagram username" required>  
    <button type="submit">Verify</button>  
</form>  
"""  
import random  @app.route("/verify", methods=["POST"])
def verify():
insta_username = request.form.get("insta")
user_id = request.form.get("user_id")

# generate random code  
code = str(random.randint(100000, 999999))  

return f"""

<h3>Verification Step</h3>  
<p>Put this code in your Instagram bio:</p>  
<h2>{code}</h2>  
<p>Then click below to check</p>  <form action="/check" method="post">  
    <input type="hidden" name="insta" value="{insta_username}">  
    <input type="hidden" name="code" value="{code}">  
    <input type="hidden" name="user_id" value="{user_id}">  
    <button type="submit">Check Verification</button>  
</form>  
"""  
@app.route("/check", methods=["POST"])  
def check():  
    insta_username = request.form.get("insta")  
    code = request.form.get("code")  
    user_id = request.form.get("user_id")  url = f"https://www.instagram.com/{insta_username}/"  

headers = {  
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  
"Accept": "text/html,application/xhtml+xml",  
"Accept-Language": "en-US,en;q=0.9"

}

res = requests.get(url, headers=headers)  
  
print("CODE:", code)  
print("FOUND:", code in res.text)  

if code and code.lower() in res.text.lower():  
    BOT_TOKEN = os.environ.get("BOT_TOKEN")  
    GUILD_ID = "1484761131657723934"  
    ROLE_ID = "1487321755151503500"  

    url = f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}/roles/{ROLE_ID}"  

    headers = {  
        "Authorization": f"Bot {BOT_TOKEN}"  
    }  

    response = requests.put(url, headers=headers)  

    if response.status_code == 204:  
        return "✅ VERIFIED & ROLE GIVEN!"  
    else:  
        return f"❌ Verified but role failed: {response.text}"  
else:  
    return "❌ Code not found in bio. Try again."

if name == "main":
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
