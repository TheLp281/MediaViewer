from flask import Flask, send_from_directory, render_template_string, request, make_response
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg', 'gif'}

def get_files():
    files = []
    for root, _, filenames in os.walk("."):
        for filename in sorted(filenames):
            if filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
                files.append(os.path.join(root, filename).replace("\\", "/"))
    return sorted(files)

@app.route('/')
def index():
    files = get_files()
    if files:
        return render_template_string(template, files=files)
    else:
        return "No media files found."

@app.route('/media/<path:filename>')
def serve_file(filename):
    directory = os.path.dirname(filename)
    file = os.path.basename(filename)
    return send_from_directory(directory, file)

@app.after_request
def add_cache_headers(response):
    path = request.path
    if path.startswith('/media/'):
        filename = os.path.basename(path)
        extension = filename.split('.')[-1].lower()
        if extension in ALLOWED_EXTENSIONS:
            response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scroll Media Viewer</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #000;
            overflow-y: auto;
        }
        .media-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .media-item {
            width: 100%;
            max-width: 600px;
            margin: 20px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        video, img {
            width: 100%;
            max-width: 100%;
            height: auto;
            object-fit: contain;
        }
    </style>
</head>
<body>
    <div class="media-container">
        {% for file in files %}
            <div class="media-item">
                {% if file.split('.')[-1].lower() == 'mp4' %}
                    <video controls src="/media/{{ file }}" autoplay muted loop></video>
                {% else %}
                    <img src="/media/{{ file }}" alt="media image">
                {% endif %}
            </div>
        {% endfor %}
    </div>
</body>
</html>
'''

app.run(port=8080)
