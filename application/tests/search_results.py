from typing import (Dict, List, Optional)

import requests
from scrapy import Selector

search_url: str = 'https://www.youtube.com/results?sp=CAM%253D&search_query={query_word}&page={page_number}'

results: List[Dict[str, list]] = list()
headers = {
    'accept-language': 'en-US,en;q=0.9,ka-GE;q=0.8,ka;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',

}

current_page: int = 15
query_word: str = 'pagode'
out_of_number_of_views: bool = False

while True:

    current_url: str = search_url.format(query_word=query_word, page_number=current_page)
    response: requests.Response = requests.get(current_url, headers=headers)
    selector: Selector = Selector(response=response)
    items: List[Selector] = selector.xpath('//ol[@class="section-list"]/li[2]/ol[@class="item-section"]/li')

    for item in items:
        # 'Playlist' in case of playlist so we must not take into account
        item_duration: Optional[str] = item.xpath('.//h3[@class="yt-lockup-title "]/span/text()').extract_first()
        # Get desired part from item duration
        # It maybe either duration, 'Playlist' or 'Channel
        item_duration = item_duration.replace('Duration:', "").replace(' ', "").replace(".", "").replace("-", "")
        # We are not interested in those cases
        if item_duration in ('Playlist', 'Channel'):
            continue
        # Get item title
        item_title: Optional[str] = item.xpath('.//h3[@class="yt-lockup-title "]/a/text()').extract_first()
        # Item channel
        channel: Optional[str] = item.xpath('.//div[@class="yt-lockup-byline "]/a/text()').extract_first()
        channel_url: Optional[str] = item.xpath('.//div[@class="yt-lockup-byline "]/a/@href').extract_first()
        print(channel, channel_url)
        # Get the url
        item_url: Optional[str] = item.xpath('.//h3[@class="yt-lockup-title "]/a/@href').extract_first()
        item_url = f'https://youtube.com{item_url}'
        print(item_url)
        # Get item views
        # None in case of playlist
        item_views: Optional[str] = item.xpath('.//div[@class="yt-lockup-meta "]/ul/li[2]/text()').extract_first()
        if item_views:
            item_views = item_views.replace(' ', "").replace(",", "").replace("views", "")
            item_views: int = int(item_views)
        # Stop crawling if the item views are smaller than 100K
        if item_views < 100000:
            out_of_number_of_views = True
            break

        print(item_title, item_duration, item_views)

    with open(f'application/tests/search_{current_page}.html', 'w') as output_file:
        output_file.write(response.text)

    if out_of_number_of_views:
        break

    current_page += 1