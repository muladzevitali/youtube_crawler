from flask import Blueprint

from .youtube_scraper_view import YouTubeCrawler

youtube_scraper = Blueprint(name="youtube_crawler", import_name=__name__, url_prefix='/rest/v1')
youtube_scraper.add_url_rule('/youtube/crawl',
                             view_func=YouTubeCrawler.as_view('youtube_crawler'),
                             methods=['GET', 'POST'])
