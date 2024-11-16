from flask import Flask,render_template, request
from flask_htmx import HTMX

import video_player


app=Flask(__name__)
htmx = HTMX(app)

videoSource = ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/editor')
def tryit():
    ('editor.html')


@app.get('/test')
def button_test():
    return 'LOL'

@app.get('/files_bar')
def files_bar_partial():
    return render_template('partials/files_bar.html')

@app.get('/get_video')
def get_video_player():
    return video_player.get_video_player_component(videoSource)

@app.get('/get_player')
def get_player_partial():
    return render_template('partials/video_editor.html')

@app.post('/update_source')
def update_video_source():
    global videoSource
    data = request.get_json()
    print(data["source"])
    videoSource = data["source"]


if __name__ == '__main__':
    app.run(debug=True)
