from flask import Flask,render_template, request, send_from_directory, jsonify
from flask_htmx import HTMX
import os
from moviepy.editor import *
import os
import logging
from functions import *

import video_player


app=Flask(__name__)
htmx = HTMX(app)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.processed_videos_dir = 'static/processed_videos'
    
    def process_video(self, video_path: str, prompt: str) -> str:
        try:
            clip = VideoFileClip(video_path)
            base_filename = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(self.processed_videos_dir, f"{base_filename}_processed.mp4")
            
            if "volume" in prompt:
                val = 0
                for i in prompt:
                    if i.isdigit():
                        val = int(i)
                if "reduce" in prompt or "decrease" in prompt:
                    clip = volume(clip, 1/val)
                else:
                    clip = volume(clip, val)
            
            if "black" in prompt or "white" in prompt:
                clip = blackAndWhite(clip)
            
            final_clip = compositeVideo(clip)
            writeEnd(final_clip, output_path)
            return output_path
            
        except Exception as e:
            logger.error(f"Processing error: {str(e)}", exc_info=True)
            raise

processor = VideoProcessor()


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


# receive video and save it to temp/videos
@app.post('/videos')
def save_video():
    file = request.files['file']
    print("Saving file: " + file.filename)
    file.save('temp/videos/' + file.filename)
    return 'temp/videos/' + file.filename


@app.post('/upload')
def upload_video():
    print("entering upload stage")
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        prompt = request.form.get('prompt', '')
        
        if video_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if video_file:
            filename = video_file.filename
            upload_path = os.path.join('static/uploads', filename)
            video_file.save(upload_path)
            
            logger.debug(f"Video saved to {upload_path}")
            processed_path = processor.process_video(upload_path, prompt)
            url_path = '/static/' + processed_path.replace('static/', '', 1)
            logger.debug(f"URL path for processed video: {url_path}")
            
            return jsonify({
                'message': 'Video processed successfully',
                'processed_video': url_path
            })
            
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)



if __name__ == '__main__':
    for directory in ['static/uploads', 'static/processed_videos']:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created directory: {directory}")
    
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
    app.run(debug=True)
