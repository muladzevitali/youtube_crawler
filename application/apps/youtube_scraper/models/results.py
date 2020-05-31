from datetime import datetime
from typing import List

from apps import database


class Result(database.Model):
    __tablename__ = 'scraper_results'
    columns_to_serialize: List[str] = ['title', 'url', 'artist_name', 'total_followers', 'views', 'youtube_id',
                                       'input_date', 'last_change_date', 'scraped_youtube_page']

    id = database.Column(database.Integer, database.Sequence('parser_results_id_seq'), primary_key=True)
    youtube_id = database.Column(database.String(20), unique=True)
    title = database.Column(database.String(1000))
    url = database.Column(database.String(1000))
    views = database.Column(database.Integer)
    duration = database.Column(database.String(20))
    artist_name = database.Column(database.String(500))
    channel = database.Column(database.String(200))
    channel_url = database.Column(database.String(1000))
    scraped_youtube_page = database.Column(database.Boolean, default=False)
    category = database.Column(database.String(200))
    song_name = database.Column(database.String(1000))
    album = database.Column(database.String(1000))
    license = database.Column(database.String(2000))
    description = database.Column(database.String(3999))
    is_family_friendly = database.Column(database.Boolean)
    date_published = database.Column(database.String(10))
    is_on_spotify = database.Column(database.Boolean, default=False)
    total_streams = database.Column(database.Integer)
    total_followers = database.Column(database.Integer)
    monthly_listeners = database.Column(database.Integer)
    artist_name_by_user = database.Column(database.Boolean)
    # For getting fields last change date
    last_change_date = database.Column(database.DateTime, default=datetime.now())
    # For getting last update from search
    last_update_date = database.Column(database.DateTime, default=datetime.now())
    input_date = database.Column(database.DateTime, default=datetime.now())
    search_word = database.Column(database.String(1000))
    result_changes = database.relationship('ScraperResultChange', backref='result', lazy='dynamic')

    def from_dict(self, **kwargs):
        """Load the model from dictionary"""
        self.youtube_id = kwargs.get('youtube_id')
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.views = kwargs.get('views')
        self.duration = kwargs.get('duration')
        self.artist_name = kwargs.get('artist_name')
        self.channel = kwargs.get('channel')
        self.channel_url = kwargs.get('channel_url')
        self.scraped_youtube_page = kwargs.get('scraped_youtube_page', False)
        self.category = kwargs.get('category')
        self.song_name = kwargs.get('song_name')
        self.album = kwargs.get('album')
        self.license = kwargs.get('license')
        self.description = kwargs.get('description', '')[:3999]
        self.is_family_friendly = kwargs.get('is_family_friendly')
        self.date_published = kwargs.get('date_published')
        self.total_followers = kwargs.get('total_followers')
        self.monthly_listeners = kwargs.get('monthly_listeners')
        self.monthly_listeners = kwargs.get('monthly_listeners')
        self.search_word = kwargs.get('search_word')
        self.last_update_date = datetime.now()

    @property
    def serialize(self) -> dict:
        """Serialize the object"""
        data: dict = dict()
        for column_name in self.columns_to_serialize:
            value = self.__getattribute__(column_name)
            data[column_name] = value

        return data

    def __repr__(self):
        return f'{self.artist_name} {self.title}'
