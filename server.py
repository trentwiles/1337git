from flask import Flask
from flask import render_template
import requests
from flask import request
from flask import redirect, url_for

app = Flask(__name__)

# Decide if you want an image proxy or not
flask_image_proxy = False
flask_image_proxy_url = "https://www.example.com/" #INCLUDE THE SLASH AT THE END!!! THIS IS IMPORTANT!!!

@app.route("/")
def main():
    return "1337 Git: Yeah its Github without trackers and crap"

@app.route("/<user>")
def user(user):
    api = requests.get("https://api.github.com/users/" + user, headers={"User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"})
    good_looking_api = api.json()
    country = good_looking_api["location"]
    name = good_looking_api["name"] # this doesn't work at the moment :(
    url = good_looking_api["blog"]
    bio = good_looking_api["bio"]
    followers =  good_looking_api["followers"]
    following = good_looking_api["following"]
    image = good_looking_api["avatar_url"]
    return render_template("user.html", user = user, country = country, link = url, bio = bio, followers=followers, following=following, image=image)
    
@app.route("/<un>/<repo>")
def repo(un, repo):
    o = requests.get("https://api.github.com/repos/" + un + "/" + repo)
    return un + repo #test

@app.route("/image-proxy")
def proxy():
    if flask_image_proxy:
        return redirect(flask_image_proxy_url + request.args.get("image"))
    else: # request.args.get
        return redirect(request.args.get("image"))

if __name__ == "__main__":
    app.run(debug=True)