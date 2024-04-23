import os
import csv
import logging
from googleapiclient.discovery import build

# comment sorting code
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import re
# comment sorting code
API_KEY = 'AIzaSyDcv_mGd8THlirQ7hJol2P3m6UeWjzZCzQ'  # Replace with your actual API key


def get_all_video_comments(api_key, video_id, **kwargs):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []

    while True:
        results = youtube.commentThreads().list(videoId=video_id, **kwargs).execute()

        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
            logging.debug(f"Comment: {comment}")


        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
        else:
            break

    return comments

def write_to_csv(comments, csv_filename):
    with open(csv_filename, 'w', encoding='utf-8', errors='replace', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Comment'])
        csv_writer.writerows([[comment] for comment in comments])









# comment sorting code

# comment sorting code
def process_video_comments(video_id):
    comments = get_all_video_comments(API_KEY, part='snippet', videoId=video_id, textFormat='plainText')
    write_to_csv(comments, 'youtube_comments.csv')

# Usage example
if __name__ == '__main__':
    process_video_comments('YOUR_VIDEO_ID')
