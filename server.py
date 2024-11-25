from flask import Flask, send_from_directory, render_template_string, request, make_response
import os
import mimetypes




app = Flask(__name__)


def get_files():
    files = []
    for root, _, filenames in os.walk("."):
        for filename in sorted(filenames):
            file_path = os.path.join(root, filename).replace("\\", "/")
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and (mime_type.startswith("image/") or mime_type.startswith("video/") or mime_type.startswith("audio/")):
                files.append(file_path)
    return sorted(files)
@app.route('/')
@app.route('/<int:index>')
def index(index=0):
    files = get_files()
    if files:
        return render_template_string(template, files=files, current_index=index)
    else:
        return "No media files found."

@app.route('/media/<path:filename>')
def serve_file(filename):
    directory = os.path.dirname(filename)
    file = os.path.basename(filename)
    return send_from_directory(directory, file)


template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Viewer</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000;
            overflow: hidden;
        }
        #media-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        .media-wrapper {
            display: none;
            width: 100%;
            height: 100%;
        }
        video, img {
            max-width: 100%;
            max-height: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
            display: block;
        }
        .nav-button {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 45%;
            background-color: transparent;
            border: none;
            cursor: pointer;
            z-index: 1000;
        }
        .prev-button {
            left: 0;
        }
        .next-button {
            right: 0;
        }
    </style>
</head>
<body>
    <div id="media-container">
        <div class="media-wrapper" id="media-wrapper">
            <video id="media" controls autoplay></video>
        </div>
        <img id="image" style="display: none;" />
        <button class="nav-button prev-button" onclick="navigate(-1)"></button>
        <button class="nav-button next-button" onclick="navigate(1)"></button>
    </div>
    <script>
        const files = {{ files|tojson }};
        let currentIndex = {{ current_index }};
        const mediaWrapper = document.getElementById('media-wrapper');
        const media = document.getElementById('media');
        const image = document.getElementById('image');

        function showMedia(index) {
            const file = files[index];
            const extension = file.split('.').pop().toLowerCase();
            if (extension === 'mp4') {
                mediaWrapper.style.display = 'block';
                image.style.display = 'none';
                media.src = '/media/' + file;
                media.load();
                media.play();
            } else {
                mediaWrapper.style.display = 'none';
                image.style.display = 'block';
                image.src = '/media/' + file;
                image.onload = () => image.style.display = 'block';
            }
        }

        function updateURL(index) {
            history.pushState(null, '', '/' + index);
        }

        function navigate(direction) {
            currentIndex = (currentIndex + direction + files.length) % files.length;
            showMedia(currentIndex);
            updateURL(currentIndex);
        }

        document.addEventListener('keydown', function(event) {
            if (event.key === 'ArrowRight') {
                navigate(1);
            } else if (event.key === 'ArrowLeft') {
                navigate(-1);
            }
        });

        showMedia(currentIndex);
    </script>
</body>
</html>
'''

app.run(port=8081)
