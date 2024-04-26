import logging
import os   
import shutil
import csv
from flask import Flask, send_file, send_from_directory,redirect, render_template, request
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

@app.route('/sort-videos', methods=['POST'])
def sortVideos():
    if request.method == 'POST':
        fanComments = "fanComments" in request.form
        hateSpeech = "hateSpeech" in request.form
        positive = "positive" in request.form
        questions = "questions" in request.form
        spam = "spam" in request.form
        suggestions = "suggestions" in request.form
        print(fanComments,hateSpeech, positive, questions,spam, suggestions)
        comments_dict = {}
        fan_comments_list = []
        hate_speech_list = []
        positive_list = []
        questions_list = []
        spam_list = []
        suggestions_list = []
        # comments_path = os.path.join(os.getcwd(), '/userdata')
        if fanComments: 
            with open(os.path.join('userdata', 'fan_comments', 'fan_comments.csv'), 'r', encoding='cp437') as file:
                fan_comments_list = file.read().splitlines()
                comments_dict['fanComments'] = fan_comments_list


        if hateSpeech: 
            with open(os.path.join('userdata', 'hate_speech', 'hate_speech.csv'), 'r', encoding='cp437') as file:
                hate_speech_list = file.read().splitlines()
                comments_dict['hateSpeech'] = hate_speech_list

        if positive: 
            with open(os.path.join('userdata', 'positive', 'positive.csv'), 'r', encoding='cp437') as file:
                positive_list = file.read().splitlines()
                comments_dict['positive'] = positive_list

        if questions: 
            with open(os.path.join('userdata', 'questions', 'questions.csv'), 'r', encoding='cp437') as file:
                print(file, 'cscfile')
                questions_list = file.read().splitlines()
                comments_dict['questions'] = questions_list
                # questions_reader = csv.reader(file)
                # next(questions_reader)  # Skip header
                # for row in questions_reader:
                #     questions_list.append(row)
                    # print(questions_list, 'questions')

        if spam: 
            with open(os.path.join('userdata', 'spam', 'spam.csv'), 'r', encoding='cp437') as file:
                spam_list = file.read().splitlines()
                comments_dict['spam'] = spam_list

        if suggestions: 
            with open(os.path.join('userdata', 'suggestions', 'suggestions.csv'), 'r', encoding='cp437') as file:
                suggestions_list = file.read().splitlines()
                comments_dict['suggestions'] = suggestions_list

        return render_template("comments.html", comments_dict=comments_dict)
            


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
           

            # return "Comments retrieved and saved successfully!"
            return render_template('sort.html', category_comments=category_word_list_pairs)
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