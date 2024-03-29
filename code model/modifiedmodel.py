import os
import csv
import subprocess
from googleapiclient.discovery import build

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

def write_to_csv(comments, video_title):
    csv_filename = f'{sanitize_filename(video_title)}_comments.csv'
    with open(csv_filename, 'w', encoding='utf-8', errors='replace', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['Username', 'Comment'])
        csv_writer.writeheader()
        csv_writer.writerows(comments)

def sanitize_filename(filename):
    # Remove characters not suitable for a filename
    return ''.join(c for c in filename if c.isalnum() or c in [' ', '_', '-'])

if __name__ == '__main__':
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_info = youtube.videos().list(part='snippet', id=VIDEO_ID).execute()
    video_title = video_info['items'][0]['snippet']['title']

    comments = get_all_video_comments(API_KEY, part='snippet', videoId=VIDEO_ID, textFormat='plainText')
    write_to_csv(comments, video_title)

def run_python_file(file_path):
    try:
        print(f"Running: {file_path}")
        subprocess.run(['python', file_path], check=True)
        print("Script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running the Python file: {e}")
    except FileNotFoundError:
        print("Python executable not found. Make sure Python is installed and in the system PATH.")


run_python_file('./Comment-Analyzer/code model/NLPmodel.py')