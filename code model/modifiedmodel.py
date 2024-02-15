import os
import csv
from googleapiclient.discovery import build

API_KEY = 'AIzaSyDcv_mGd8THlirQ7hJol2P3m6UeWjzZCzQ'  # Replace with your actual API key
VIDEO_ID = 'vQhHzkoNZaQ'  # Replace with the YouTube video ID

def get_all_video_comments(api_key, **kwargs):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []

    while True:
        results = youtube.commentThreads().list(**kwargs).execute()

        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if there are more comments
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

if __name__ == '__main__':
    comments = get_all_video_comments(API_KEY, part='snippet', videoId=VIDEO_ID, textFormat='plainText')
    write_to_csv(comments, 'youtube_comments.csv')