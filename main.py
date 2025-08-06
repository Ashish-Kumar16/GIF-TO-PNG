from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageSequence
import io

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GIF to PNG Converter</title>
<style>
  body { font-family: Arial, sans-serif; background: #f7f7f7; }
  .container { max-width: 400px; margin: 60px auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); padding: 30px 20px; text-align: center; }
  input[type="file"] { margin: 20px 0; }
  button { background: black; color: #fff; border: none; padding: 12px 24px; border-radius: 5px; font-size: 16px; cursor: pointer; margin-bottom: 20px; }
  #preview img { margin-top: 20px; max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
</style>
</head>
<body>
<div class="container">
  <h1>GIF to PNG Converter</h1>
  <form id="uploadForm" method="post" enctype="multipart/form-data" action="/convert">
    <input type="file" name="gif" accept="image/gif" required>
    <br>
    <button type="submit">Convert & Download PNG</button>
  </form>
  <div id="preview"></div>
  {% if url %}
    <div id="preview">
      <img src="{{ url }}" alt="Last Frame PNG">
      <br>
      <a href="{{ url }}" download="output.png">Download PNG</a>
    </div>
  {% endif %}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
  return render_template_string(HTML)

@app.route('/convert', methods=['POST'])
def convert():
  file = request.files['gif']
  if not file:
      return "No file uploaded", 400

  img_bytes = io.BytesIO(file.read())
  with Image.open(img_bytes) as im:
      frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
      output = io.BytesIO()
      frames[-1].save(output, format='PNG')
      output.seek(0)
      return send_file(output, mimetype='image/png', as_attachment=True, download_name='output.png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
