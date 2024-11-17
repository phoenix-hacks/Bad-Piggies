from flask import Flask,render_template, request, send_from_directory, jsonify, url_for
from flask_htmx import HTMX
import os
from moviepy.editor import *
import os
import logging
from ollama_functionality import llmotpt
from werkzeug.utils import secure_filename
import video_player
import shutil


app=Flask(__name__)
htmx = HTMX(app)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.processed_videos_dir = 'static/processed_videos'
    
    def process_video(self, video_path: str, prompt: str) -> str:
        try:
            print("K")
            clip = VideoFileClip(video_path)
            base_filename = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(self.processed_videos_dir, f"{base_filename}_processed.mp4")
            llmotpt(prompt,video_path,output_path)
            
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
            print(video_file)
            filename = video_file.filename
            upload_path = os.path.join('static/uploads/video.mp4')
            video_file.save(upload_path)
            shutil.copy(upload_path, 'static/processed_videos/video_processed.mp4')
            
            logger.debug(f"Video saved to {upload_path}")
            
            return jsonify({
                'message': 'Video uploaded successfully',
                'processed_video': upload_path
        })
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.get('/static/<path:filename>')
def serve_static(filename):
    return url_for('static', filename=filename)
    
@app.post('/process')
def process():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        prompt = request.form.get('prompt', '')

        print('Prompt given: ' + prompt)
        
        if video_file.filename == '':
            return jsonify({'error': 'No selected file'}), 401
        
        if video_file:
            # Ensure the upload directory exists
            os.makedirs('static/processed_videos', exist_ok=True)
            
            # Secure the filename and save the file
            filename = video_file.filename
            os.makedirs('static/uploads', exist_ok=True)
            upload_path = os.path.join('static/uploads', filename)

            if os.path.exists('static/processed_videos/video_processed.mp4'):
                shutil.copy2('static/processed_videos/video_processed.mp4', 'static/uploads/video.mp4')
                print('Moved previously processed video')
            
            # Process the video
            print('Process: ' + upload_path)
            processed_path = processor.process_video(upload_path, prompt)
            url_path = processed_path#.replace('static/', '', 1)
            
            logger.debug(f"URL path for processed video: {url_path}")
            
            return jsonify({
                'message': 'Video processed successfully',
                'processed_video': url_path
            })
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    for directory in ['static/uploads', 'static/processed_videos']:
        os.makedirs(directory, exist_ok=True)
        
        logger.debug(f"Created directory: {directory}")
    
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
    app.run(debug=True)
