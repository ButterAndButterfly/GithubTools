import sys
sys.path.append("..")
from core.github import *
from core import github_star_history
from flask import Flask, Response, request, render_template
import requests
import json, os
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/s/<path:path>')
@app.route('/f/<path:path>')
def starsAndForks(path):
    token = os.getenv('MY_GITHUB_TOKEN')
    path = unquote(path)
    names = path.split("+");
    print(names)
    result = {"stars": 0, "forks": 0}
    for name in names:
        if name == "":
            break
        data = query_total(name, token)
        result["stars"] += data["stars"]
        result["forks"] += data["forks"]
    return json.dumps(result, ensure_ascii=False)

@app.route('/h/<name>/<repo>')
def star_history(name, repo):
    token = os.getenv('MY_GITHUB_TOKEN')
    print(repo)
    
    try:
        div = request.args.get('div')
        if div:
            div = int(div)
        else:
            div = 4
        data = github_star_history.draw(name, repo, token, div)
        headers={
            "Content-Transfer-Encoding": 'binary',
            "cache-control": 'max-age=31536000',
            "Content-Disposition": 'inline; filename="star-history.jpg"',
        }
        return Response(data, mimetype="image/png", headers=headers)
    except exception as e:
        return Response("Error Happens: \r\n" + e, mimetype="text/plain")
 
if __name__ == "__main__":
    #.environ['MY_GITHUB_TOKEN'] = token
    app.run(debug = True)
