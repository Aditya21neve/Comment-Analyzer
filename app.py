# app.py

from flask import Flask, send_file, send_from_directory, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/get_comments', methods=['POST'])
# def get_comments():
#     if request.method == 'POST':
#         youtube_url = request.form['url']
#         video_id = extract_video_id(youtube_url)
#         process_video_comments(video_id)
#         return 'Comments retrieved and saved to CSV successfully!'
#     else:
#         return 'Method Not Allowed', 405




# https://youtu.be/PFnJvUNK6t0?si=tFouUcQ5bHhgsKP8