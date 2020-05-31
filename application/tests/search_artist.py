import requests
from scrapy import Selector

headers = {
    'accept-language': 'en-US,en;q=0.9,ka-GE;q=0.8,ka;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',

}

# url = 'https://www.youtube.com/watch?v=zfYrxwU4Lrg'
url = 'https://www.youtube.com/watch?v=ztkOujnq4gQ'

response = requests.get(url, headers=headers)
with open('application/tests/video_page_2.html', 'w') as output_file:
    output_file.write(response.text)
selector = Selector(response)

category_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                   '//li[h4[normalize-space(text())="Category"]]')
if category_selector:
    print(category_selector.xpath("./ul//li//text()").extract())

song_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                               '//li[h4[normalize-space(text())="Song"]]')
if song_selector:
    print(song_selector.xpath("./ul//li//text()").extract_first())

artist_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                 '//li[h4[normalize-space(text())="Artist"]]')
if artist_selector:
    print(artist_selector.xpath("./ul//li//text()").extract_first())

album_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                '//li[h4[normalize-space(text())="Album"]]')
if album_selector:
    print(album_selector.xpath("./ul//li//text()").extract_first())

license_selector = selector.xpath('//div[@id="watch7-main"]//ul[@class="watch-extras-section"]'
                                  '//li[h4[contains(normalize-space(text()), "Licensed to")]]')
if license_selector:
    print(license_selector.xpath("./ul//li//text()").extract_first())

meta_selector = selector.xpath('//div[@id="watch7-main"]/div[@id="watch7-content"]')
description = meta_selector.xpath('.//meta[@itemprop="description"]/@content').extract_first()
is_family_friendly = meta_selector.xpath('.//meta[@itemprop="isFamilyFriendly"]/@content').extract_first()
date_published = meta_selector.xpath('.//meta[@itemprop="datePublished"]/@content').extract_first()

print(description, is_family_friendly, date_published)
