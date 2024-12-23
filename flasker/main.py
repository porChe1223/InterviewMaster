from flasker import app
from flask import request, jsonify, render_template
import os
import subprocess

@app.route('/')
def main():
    text = 'Hello, World!'
    return render_template(
        'main.html', text = text # 引数はいくつでも追加可能
    )

app.config['UPLOAD_FOLDER'] = 'uploads'

# Video upload route
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(filepath)

    # Run OpenFace FeatureExtraction
    output_path = filepath.replace('.mp4', '_output.csv')
    command = [
        './OpenFace/build/bin/FeatureExtraction',
        '-f', filepath,
        '-o', output_path
    ]
    try:
        subprocess.run(command, check=True)
        return jsonify({'message': 'Processing complete', 'output': output_path})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Processing failed: {e}'}), 500

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug = True)
