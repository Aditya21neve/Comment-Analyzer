# app.py

from flask import Flask, request

app = Flask(__name__)

@app.route('/get_comments', methods=['POST'])
def get_comments():
    if request.method == 'POST':
        youtube_url = request.form['url']
        video_id = extract_video_id(youtube_url)
        process_video_comments(video_id)
        return 'Comments retrieved and saved to CSV successfully!'
    else:
        return 'Method Not Allowed', 405

if __name__ == '__main__':
    app.run(debug=True)
