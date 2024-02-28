import os
import csv
from googleapiclient.discovery import build
from textblob import TextBlob


API_KEY = 'AIzaSyDcv_mGd8THlirQ7hJol2P3m6UeWjzZCzQ'  # Replace with your actual API key
VIDEO_ID = 'vQhHzkoNZaQ'  # Replace with the YouTube video ID


def get_all_video_comments(api_key, **kwargs):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []

    while True:
        results = youtube.commentThreads().list(**kwargs).execute()

        for item in results.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            username = comment['authorDisplayName']
            text_display = comment['textDisplay']
            comments.append({'Username': username, 'Comment': text_display})

        # Check if there are more comments
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
        else:
            break

    return comments

def write_to_csv(comments, video_title, output_folder='comments'):
    os.makedirs(output_folder, exist_ok=True)
    csv_filename = os.path.join(output_folder, f'{sanitize_filename(video_title)}_comments.csv')
    
    with open(csv_filename, 'w', encoding='utf-8', errors='replace', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['Username', 'Comment', 'Category'])
        csv_writer.writeheader()
        csv_writer.writerows(comments)

def categorize_comments(comments):
    categorized_comments = []

    for comment in comments:
        text = comment['Comment']
        category = categorize_text(text)
        comment['Category'] = category
        categorized_comments.append(comment)

    return categorized_comments

def categorize_text(text):
    # Simple rule-based categorization
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0.5:
        return 'Positive Comment'
    elif sentiment_score < -0.5:
        return 'Hate Speech'
    elif 'collaboration' in text.lower():
        return 'Collaboration Request'
    elif '?' in text:
        return 'Question'
    elif 'spam' in text.lower():
        return 'Spam'
    else:
        return 'Uncategorized'

def sanitize_filename(filename):
    # Remove characters not suitable for a filename
    return ''.join(c for c in filename if c.isalnum() or c in [' ', '_', '-'])

if __name__ == '__main__':
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_info = youtube.videos().list(part='snippet', id=VIDEO_ID).execute()
    video_title = video_info['items'][0]['snippet']['title']

    comments = get_all_video_comments(API_KEY, part='snippet', videoId=VIDEO_ID, textFormat='plainText')
    categorized_comments = categorize_comments(comments)
    write_to_csv(categorized_comments, video_title)
