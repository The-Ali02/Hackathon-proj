import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from spot_deepfakes import displayOutput, clearDirectories
import time
from youtube_scrapper import youtubescrape
app = Flask(__name__)

UPLOAD_FOLDER = r'C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/input'
INPUT = r'C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/output'
SHORTS=r'C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/youtube_videos'
app.config['INPUT'] = INPUT
app.config['SHORTS'] = SHORTS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv', 'mov'} 
# clearDirectories(r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/input", r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/src/buffer" , r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/output")
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    # clearDirectories(r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/input", r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/src/buffer" , r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/output")
    # time.sleep(4)

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return render_template('index.html', filename=filename)

    return render_template('index.html')

@app.route('/play_video')
def play_video():
    input_video_folder = app.config['INPUT']
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

    if not video_files:
        return "No video files found in the INPUT folder."

    input_video_path = os.path.join(input_video_folder, video_files[0])
    return send_file(input_video_path, mimetype='video/mp4')
    
@app.route('/process', methods=['GET','POST'])
def play_videos():
    displayOutput(True)
    return render_template('index.html')



@app.route('/pro', methods=['GET','POST'])
def play():
    input_video_folder = app.config['INPUT']
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

    if not video_files:
        return "No video files found in the INPUT folder."

    input_video_path = os.path.join(input_video_folder, video_files[0])
    return send_file(input_video_path, mimetype='video/mp4')

# @app.route('/shorts')
# def shorts():
#     youtubescrape()
#     # video_folder = os.path.join(app.static_folder, 'youtube_videos')  # Adjust the folder path accordingly
#     video_folder = r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/youtube_videos"
#     video_filenames = [filename for filename in os.listdir(video_folder) if filename.endswith(('.mp4', '.mkv', '.webm'))]
#     return jsonify(video_filenames)
    

# @app.route('/disp')
# def disp():
#     return render_template('videos.html')

@app.route('/disp')
def filenamess():
    folder_path = r"C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/youtube_videos"  # Replace with your folder path
    file_names = get_file_names(folder_path)
    # return render_template('videos.html', file_names=file_names)
    return render_template('videos.html', file_names=file_names)

def get_file_names(folder_path):
    try:
        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return file_names
    except OSError as e:
        print(f"Error reading folder: {e}")
        return []

# @app.route('/play_shorts')
# def play_shortsssss():
#     input_video_folder = app.config['SHORTS']
#     video_files = [f for f in os.listdir(input_video_folder) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

#     if not video_files:
#         return "No video files found in the INPUT folder."

#     input_video_path = os.path.join(input_video_folder, video_files[0])
#     return send_file(input_video_path, mimetype='video/mp4')
@app.route('/play_shorts_list')
def play_shorts_list():
    input_video_folder = app.config['SHORTS']
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

    if not video_files:
        return jsonify({"error": "No video files found in the INPUT folder."})
    video_list = [{'index': i, 'file': video_files[i]} for i in range(len(video_files))]
    return jsonify(video_list)

@app.route('/play_shorts')
def play_shorts():
    index = int(request.args.get('index', 0))
    input_video_folder = app.config['SHORTS']
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

    if not video_files:
        return "No video files found in the INPUT folder."

    if index < 0 or index >= len(video_files):
        return "Invalid video index."

    input_video_path = os.path.join(input_video_folder, video_files[index])
    return send_file(input_video_path, mimetype='video/mp4')
if __name__ == '__main__':
    app.run(debug=True)