import logging
import os
import shutil
from flask import Flask, send_file, send_from_directory, render_template, request
from model import process_video_comments, get_all_video_comments, API_KEY, write_to_csv,sort_comment_csv

app = Flask(__name__)

# Set up logging configuration before any logging statements
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    if os.path.exists('youtube_comments.csv'):
        # If it exists, delete the file
        os.remove('youtube_comments.csv')
    if os.path.exists('userdata'):
    # If it exists, delete the entire folder and its contents
        shutil.rmtree('userdata')
    return render_template('index.html')

@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/get_comments', methods=['POST'])
def get_comments():
    if request.method == 'POST':
        video_url = request.form['url']
        video_id = extract_video_id(video_url)
        if video_id:
            process_video_comments(video_id)
            categories = ['questions', 'spam', 'fan_comments', 'hate_speech', 'positive', 'suggestions']
            category_word_list_pairs = []
            for category in categories:
                ideal_word_list_file = os.path.join(os.getcwd(), 'data', f'{category}.txt')
                category_word_list_pairs.append((category, ideal_word_list_file))

            comments_file = 'youtube_comments.csv'
            sort_comment_csv(comments_file, category_word_list_pairs)
           

            return "Comments retrieved and saved successfully!"
        else:
            flash('Invalid YouTube URL. Please provide a valid URL.', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid request method.', 'error')
        return redirect(url_for('index'))
# 

# 
def extract_video_id(video_url):
    if 'youtu.be' in video_url:
        # If the URL is in the short format like 'https://youtu.be/PFnJvUNK6t0?si=tFouUcQ5bHhgsKP8'
        video_id = video_url.split('/')[-1].split('?')[0]
    else:
        # If the URL is in the long format like 'https://www.youtube.com/watch?v=PFnJvUNK6t0&si=tFouUcQ5bHhgsKP8'
        video_id = video_url.split('v=')[-1].split('&')[0]
    # logging.debug(f"Extracted video key: {video_id}")
    return video_id

def process_video_comments(video_id):
    comments = get_all_video_comments(API_KEY, video_id=video_id, part='snippet', textFormat='plainText')
    write_to_csv(comments, 'youtube_comments.csv')


if __name__ == '__main__':
    app.run(debug=True)

# https://youtu.be/PFnJvUNK6t0?si=tFouUcQ5bHhgsKP8
