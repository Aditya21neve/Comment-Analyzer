import os
import csv
import logging
from googleapiclient.discovery import build

# comment sorting code

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






def sort_comment_csv(comments_file, category_word_list_pairs):
    for category, ideal_word_list_file in category_word_list_pairs:
        # Read the ideal word list from the file
        with open(ideal_word_list_file, 'r') as file:
            ideal_words = file.read().splitlines()

        # Create a new directory for storing categorized comments if it doesn't exist
        output_dir = os.path.join('userdata', category)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the output CSV file in write mode
        with open(os.path.join(output_dir, f'{category}.csv'), 'w', newline='', encoding='utf-8') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow(['Comment'])

            # Read comments from the input CSV file
            with open(comments_file, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # Skip header
                for row in reader:
                    comment = row[0]
                    # Check if any word from the ideal word list is present in the comment
                    if any(word.lower() in comment.lower() for word in ideal_words):
                        writer.writerow([comment])
  
# comment sorting code
def process_video_comments(video_id):
    comments = get_all_video_comments(API_KEY, part='snippet', videoId=video_id, textFormat='plainText')
    write_to_csv(comments, 'userdata/youtube_comments.csv')

# Usage example
if __name__ == '__main__':
    process_video_comments('YOUR_VIDEO_ID')
    comments_file = 'userdata/youtube_comments.csv'
    

    categories = ['question', 'spam', 'fan_comments', 'hate_speech', 'positive', 'suggestions']
    category_word_list_pairs = [(category, os.path.join('data', f'{category}.txt')) for category in categories]
    print(category_word_list_pairs, '==================================categorylist================================')
    sort_comment_csv(comments_file, category_word_list_pairs)
    