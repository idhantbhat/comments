from flask import Flask, render_template, redirect, url_for, flash, request
from functools import wraps
from datetime import datetime, timedelta
from flask import abort
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from config import APIKEY

api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=APIKEY)

def CommentGet(vidID, KWord):
    xylans = 1
    pattern = r'(?<=v=)[\w-]+'
    match = re.search(pattern, vidID)
    if match:
        video_id = match.group()
    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100
    ).execute()
    comments = []
    for i in range(len(response['items'])):
        comment = response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
        if f"{KWord}".lower() in comment.lower():
            comments.append(comment)
    return comments
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/comments', methods=['POST'])
def comments():
    commentz = CommentGet(f"{request.form['url']}", f"{request.form['KWord']}")
    return render_template("comments.html", commentz=commentz)

if __name__ == "__main__":
    app.run(debug=True)

