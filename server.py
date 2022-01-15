from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)

@app.route("/")
def main():
    return "1337 Git: Yeah its Github with trackers and crap"

@app.route("/user/<user>")
def user(user):
    api = requests.get("https://api.github.com/users/" + user, headers={"User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"})
    good_looking_api = api.json()
    country = good_looking_api["location"]
    name = good_looking_api["site_admin"]
    url = good_looking_api["blog"]
    return render_template("user.html", user = user, country = country, link = url)
    
if __name__ == "__main__":
    app.run(debug=True)