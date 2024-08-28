from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os
from PIL import Image
from moviepy.editor import VideoFileClip

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the icons folder
ICONS_FOLDER = 'icons'
if not os.path.exists(ICONS_FOLDER):
    os.makedirs(ICONS_FOLDER)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/file_icon/<filename>')
def file_icon(filename):
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext == '.zip':
        icon_path = os.path.join(ICONS_FOLDER, 'zip-icon.png')
    else:
        icon_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.png')
    return send_file(icon_path, mimetype='image/png')

@app.route('/thumbnail/<filename>')
def thumbnail_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    thumbnail_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails')
    if not os.path.exists(thumbnail_folder):
        os.makedirs(thumbnail_folder)
    thumbnail_path = os.path.join(thumbnail_folder, filename)
    if not os.path.exists(thumbnail_path):
        img = Image.open(image_path)
        img.thumbnail((100, 100), resize=True)  # <--- Add resize=True
        img.save(thumbnail_path)
    return send_file(thumbnail_path, mimetype='image/png')

@app.route('/video_thumbnail/<filename>')
def video_thumbnail(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    thumbnail_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails')
    if not os.path.exists(thumbnail_folder):
        os.makedirs(thumbnail_folder)
    thumbnail_path = os.path.join(thumbnail_folder, filename + '.png')
    if not os.path.exists(thumbnail_path):
        clip = VideoFileClip(video_path)
        img = clip.get_frame(1)
        img.save(thumbnail_path)
    return send_file(thumbnail_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)