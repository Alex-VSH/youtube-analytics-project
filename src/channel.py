import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        info_channel = json.dumps(channel, indent=2, ensure_ascii=False)
        info_channel_json = json.loads(info_channel)
        self.title = info_channel_json['items'][0]['snippet']['title']
        self.description = info_channel_json['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subs_count = int(info_channel_json['items'][0]['statistics']['subscriberCount'])
        self.video_count = info_channel_json['items'][0]['statistics']['videoCount']
        self.view_count = info_channel_json['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subs_count + other.subs_count

    def __sub__(self, other):
        return self.subs_count - other.subs_count

    def __gt__(self, other):
        return self.subs_count > other.subs_count

    def __ge__(self, other):
        return self.subs_count >= other.subs_count

    def __lt__(self, other):
        return self.subs_count < other.subs_count

    def __le__(self, other):
        return self.subs_count <= other.subs_count

    def __eq__(self, other):
        return self.subs_count == other.subs_count

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        Channel.printj(channel)

    def to_json(self, file_name):
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        with open(os.path.join(file_name), 'w') as file:
            file.write(json.dumps(channel, indent=2, ensure_ascii=False))
