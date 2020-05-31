from typing import (List, Optional, Dict)

import requests
from scrapy import Selector

from apps import application
from apps.youtube_scraper.models import Result
from source.loggers import logger


class YoutubeScraper:
    headers = {
        'accept-language': 'en-US,en;q=0.9,ka-GE;q=0.8,ka;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
    }

    def __init__(self, search_word: str, min_views: Optional[int] = 10 ** 6, max_views: Optional[int] = 2 * 10 ** 6):
        self.search_word: str = search_word
        self.search_url: str = 'https://www.youtube.com/' \
                               'results?sp=CAM%253D&search_query={search_word}&page={page_number}'
        # Number of views to cut from
        self.upper_bound: int = max_views
        # Number of view to cut to
        self.lower_bound: int = min_views

    def run(self) -> Optional[List[dict]]:
        """Run the parser"""
        current_page: int = 1
        out_of_number_of_views: bool = False
        results: List[dict] = list()
        logger.info(f'search videos in youtube with name: {self.search_word}')

        while True:
            # Format the url
            current_url: str = self.search_url.format(search_word=self.search_word, page_number=current_page)
            # Send the request
            response: requests.Response = requests.get(current_url, headers=self.headers)
            # Cast response to selector
            selector: Selector = Selector(response=response)
            # Get listed items from search result page
            items: List[Selector] = selector.xpath('//ol[@class="section-list"]/li[2]/ol[@class="item-section"]/li')

            for item in items:
                try:
                    # 'Playlist' in case of playlist so we must not take into account
                    duration: Optional[str] = item.xpath('.//h3[@class="yt-lockup-title "]/span/text()').extract_first()
                    # Get desired part from item duration
                    # It maybe either duration, 'Playlist', 'Channel, Live(None in case of Live)
                    if not duration:
                        continue
                    duration = duration.replace('Duration:', "").replace(' ', "").replace(".", "").replace("-", "")
                    # We are not interested in those cases
                    if duration in ('Playlist', 'Channel'):
                        continue
                    # Get item views
                    # None in case of playlist
                    views: Optional[str] = item.xpath(
                        './/div[@class="yt-lockup-meta "]/ul/li[2]/text()').extract_first()
                    if views:
                        views = views.replace(' ', "").replace(",", "").replace("views", "")
                        views: int = int(views)
                    # If item views more than 10M do not include in results
                    if views > self.upper_bound:
                        continue
                    # Stop crawling if the item views are smaller than 100K
                    if views < self.lower_bound:
                        out_of_number_of_views = True
                        break
                    # Get item title
                    title: Optional[str] = item.xpath('.//h3[@class="yt-lockup-title "]/a/text()').extract_first()
                    # Get the url
                    url: Optional[str] = item.xpath('.//h3[@class="yt-lockup-title "]/a/@href').extract_first()
                    url = f'https://youtube.com{url}'
                    # Channel information
                    channel: Optional[str] = item.xpath('.//div[@class="yt-lockup-byline "]/a/text()').extract_first()
                    channel_url: Optional[str] = item.xpath(
                        './/div[@class="yt-lockup-byline "]/a/@href').extract_first()
                    youtube_id = url.split('=')[-1]
                    # Make a dict result for further processing
                    result: dict = {'title': title,
                                    'youtube_id': youtube_id,
                                    'url': url,
                                    'views': views,
                                    'duration': duration,
                                    'channel': channel,
                                    'search_word': self.search_word,
                                    'channel_url': f'https://youtube.com{channel_url}'}

                    results.append(result)
                except TypeError:
                    logger.error(f'TypeError on url {current_url} ')

            # If number of views is smaller than wanted exit from while loop
            if out_of_number_of_views:
                break

            current_page += 1
        # Get artist names already in the database
        youtube_ids: List[str] = [item['youtube_id'] for item in results]
        with application.app_context():
            artist_results: List[Result] = Result.query.filter(Result.youtube_id.in_(youtube_ids)).all()
            id_to_artist_mapper: Dict[str: str] = {item.youtube_id: item.serialize for item in artist_results}

        # Update results list
        for item in results:
            youtube_id = item['youtube_id']

            item.update(id_to_artist_mapper.get(youtube_id, {}))

        results: List[dict] = [self.get_artist_pool(result) for result in results]

        logger.info(f'run youtube search on word: {self.search_word} with {current_page} pages')

        return results

    def get_artist_pool(self, result: dict) -> dict:
        """Get  artist with multiprocessing handler"""
        # If artist name is already in the
        if result.get('scraped_youtube_page'):
            return result

        video_metadata = self.get_artist(video_url=result['url'])
        result.update(video_metadata)

        return result

    # TODO better logic
    def get_artist(self, video_url) -> Optional[Dict]:
        """Get artist from video meta"""

        return self.scrape_video_page(url=video_url)

    def scrape_video_page(self, url) -> Dict[str, str]:
        """Parse video page to get the metadata"""
        # Base metadata for future acknowledging of scraper status in view
        video_metadata = dict(scraped_youtube_page=True, existing=False)
        # Get the video page
        response: requests.Response = requests.get(url, headers=self.headers)
        # If some problem with request
        if not response.status_code == 200:
            video_metadata['scraped_youtube_page'] = False
            logger.error(f'error getting page: {url}')

            return video_metadata

        selector: Selector = Selector(response)
        # Get category of the video
        category_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                           '//li[h4[normalize-space(text())="Category"]]')
        if category_selector:
            categories: list = category_selector.xpath("./ul//li//text()").extract()
            video_metadata['category'] = ','.join(categories)
        # Get song if presented
        song_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                       '//li[h4[normalize-space(text())="Song"]]')
        if song_selector:
            song_name: Optional[str] = song_selector.xpath("./ul//li//text()").extract_first()
            video_metadata['song'] = song_name
        # Get artist if presented
        artist_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                         '//li[h4[normalize-space(text())="Artist"]]')
        if artist_selector:
            artist_name: Optional[str] = artist_selector.xpath("./ul//li//text()").extract_first()
            video_metadata['artist_name'] = artist_name
        # Get album if presented
        album_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                        '//li[h4[normalize-space(text())="Album"]]')
        if album_selector:
            album: Optional[str] = album_selector.xpath("./ul//li//text()").extract_first()
            video_metadata['album'] = album
        # Get licensor if selected
        license_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                          '//li[h4[contains(normalize-space(text()), "Licensed to")]]')
        if license_selector:
            license_: Optional[str] = license_selector.xpath("./ul//li//text()").extract_first()
            video_metadata['license'] = license_

        meta_selector = selector.xpath('//div[@id="watch7-main"]/div[@id="watch7-content"]')
        if meta_selector:
            # Video description
            description = meta_selector.xpath('.//meta[@itemprop="description"]/@content').extract_first()
            video_metadata['description'] = description
            # Is video family friendly
            is_family_friendly = meta_selector.xpath('.//meta[@itemprop="isFamilyFriendly"]/@content').extract_first()
            video_metadata['is_family_friendly'] = is_family_friendly == 'True'
            # Video published date
            date_published = meta_selector.xpath('.//meta[@itemprop="datePublished"]/@content').extract_first()
            video_metadata['date_published'] = date_published

        return video_metadata
