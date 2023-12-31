from flask import Blueprint, render_template, current_app, request
import requests
from isodate import parse_duration
import math

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    videos =[]
    if request.method == 'POST':
        text = request.form.get('search')

        search_params = {
            'key' : current_app.config['API_KEY'],
            'q' : text,
            'part' : 'snippet',
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)
        
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'key' : current_app.config['API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet, contentDetails',
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']
        for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : (parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'title' : result['snippet']['title']
            }
            videos.append(video_data)

    return render_template('index.html', videos=videos)