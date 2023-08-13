import os
from datetime import timedelta
import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')


class PlayList:
    def __init__(self, playlist_id):
        """Функция инициализации плейлиста"""
        self.playlist_id = playlist_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='snippet',
                                                            maxResults=50,
                                                            ).execute()
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id
        self.playlist_info = youtube.playlists().list(id=playlist_id,
                                                      part='snippet',
                                                      ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.video_ids: list[str] = [video['snippet']['resourceId']['videoId'] for video in
                                     self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()
        self.total_duration_time = timedelta(hours=0, minutes=0)

    def show_best_video(self):
        """Функция выводит ссылку на самое популярное по лайкам видео
        в плейлисте, предварительно создавая список со всеми значениями лайков, а затем
        находит по максимальному значению из списка само видео"""
        list_of_likes = []
        for video in self.video_response['items']:
            list_of_likes.append(int(video['statistics']['likeCount']))
        for video in self.video_response['items']:
            if max(list_of_likes) == int(video['statistics']['likeCount']):
                return 'https://youtu.be/' + video['id']

    @property
    def total_duration(self):
        """Функция возвращает суммарнуб длительность плейлиста"""
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            self.total_duration_time += duration
        return self.total_duration_time

