if __name__ == '__main__':
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_info = youtube.videos().list(part='snippet', id=VIDEO_ID).execute()
    video_title = video_info['items'][0]['snippet']['title']

    comments = get_all_video_comments(API_KEY, part='snippet', videoId=VIDEO_ID, textFormat='plainText')
    write_to_csv(comments, video_title)

    def run_python_file(file_path):
        try:
            subprocess.run(['python', file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running the Python file: {e}")
        except FileNotFoundError:
            print("Python executable not found. Make sure Python is installed and in the system PATH.")
        
run_python_file('NLPmodel.py')