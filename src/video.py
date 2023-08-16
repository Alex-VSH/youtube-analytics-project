import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')


class Video:

    def __init__(self, video_id):
        self.video_id = video_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id
                                                    ).execute()
        try:
            self.title = self.video_response['items'][0]['snippet']['title']
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
            self.url = 'https://youtu.be/' + self.video_id
        except IndexError:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.url = None

    #
    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
