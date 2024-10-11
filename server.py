from http.client import OK
from flask import Flask
from flask import render_template
from importlib_metadata import version
import requests
from flask import request
from flask import redirect
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from flask import Response

md = (
    MarkdownIt()
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .enable('table')
)

app = Flask(__name__)

app_version = "beta-1.0.0"

@app.route("/")
def main():
    return render_template("home.html", version = app_version)

@app.route("/<user>")
def user(user):
    api = requests.get("https://api.github.com/users/" + user, headers={"User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"})
    try:
        readme = requests.get("https://raw.githubusercontent.com/" + user + "/" + user+ "/master/README.md")
        if readme == "404: Not Found":
            final_readme = "This user has choose not to set up a readme."
        else:
            final_readme = md.render(readme.text)
    except:
        final_readme = "This user has choose not to set up a readme."
    good_looking_api = api.json()
    try:
        country = good_looking_api["location"]
    except:
        country = "Unknown"

    url = good_looking_api["blog"]
    bio = good_looking_api["bio"]
    followers =  good_looking_api["followers"]
    following = good_looking_api["following"]
    image = good_looking_api["avatar_url"]
    try:
        if request.args.get('tab') == "repos":
            o = requests.get("https://api.github.com/users/" + user + "/repos")
            data = o.json()
            return render_template("user-repos.html", repos = data, user = user)
        else:
            return render_template("user.html", user = user, country = country, link = url, bio = bio, followers=followers, following=following, image=image, readme = final_readme)
    except:
        return render_template("user.html", user = user, country = country, link = url, bio = bio, followers=followers, following=following, image=image, readme = final_readme)
@app.route("/<un>/<repo>")
def repo(un, repo):
    o = requests.get("https://api.github.com/repos/" + un + "/" + repo)
    contents = requests.get("https://api.github.com/repos/" + un + "/" + repo + "/contents/")
    json = contents.json()
    if contents.status_code == 404:
        return "404: Not found" # maybe add a template here in the future
    return render_template("repo.html", un = un, repo = repo, json = json, o = o.json())

@app.route("/<un>/<repo>/issues")
def issues(un, repo):
    o = requests.get("https://api.github.com/repos/" + un + "/" + repo + "/issues")
    data = o.json()
    return render_template("issues.html", issues = data, un = un, repo = repo)

@app.route("/<un>/<repo>/stargazers")
def stars(un, repo):
    o = requests.get("https://api.github.com/repos/" + un + "/" + repo + "/stargazers")
    data = o.json()
    return render_template("stars.html", stars = data, un = un, repo = repo)

@app.route("/<un>/<repo>/issues/<id>")
def getissues(un, repo, id):
    o = requests.get("https://api.github.com/repos/" + un + "/" + repo + "/issues/" + id)
    data = o.json()
    return render_template("getissue.html", issues = data, un = un, repo = repo, id = id, render=md.render)

@app.route("/explore")
def explore():
    o = requests.get("https://api.github.com/search/repositories?q=code&sort=stars&order=desc&per_page=100")
    data = o.json()
    return render_template("trending.html", items = data["items"])

@app.route("/image-proxy")
def proxy():
    return redirect("https://external-content.duckduckgo.com/iu/?u=" + request.args.get("image"))


@app.route("/robots.txt")
def bots():
    return Response(render_template("robots.txt"), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)