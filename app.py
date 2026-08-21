import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50MB Max Upload Size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

HTML_TEMPLATE = """
<!doctype html>
<title>Media Uploader</title>
<h2>Upload Image or Video</h2>
<form method="post" action="/upload" enctype="multipart/form-data">
	<input type=file name=file required>
	<input type=submit value=Upload>
</form>
<h2>Uploaded Files</h2>
<ul>
  {% for file in files %}
     <li><a href="/uploads/{{ file }}" target="_blank">{{ file }}</a></li>
  {% else %}
    <li>No files uploaded yet.</li>
  {% endfor %}
</ul>
"""

@app.route('/')
def index():
	files = os.listdir(app.config['UPLOAD_FOLDER'])
	return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_files():
	if 'file' not in request.files:
	   return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
	   return redirect(request.url)
	if file and allowed_file(file.filename):
	   filename = secure_filename(file.filename)
	   file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	   return redirect(url_for('index'))
	return "Invalid file type", 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=80)
