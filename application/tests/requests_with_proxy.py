import requests

proxies_dict = {'http': 'http://lum-customer-hl_cd462c02-zone-static:afcf8w8d63n9@zproxy.lum-superproxy.io:22225',
                'https': 'http://lum-customer-hl_cd462c02-zone-static:afcf8w8d63n9@zproxy.lum-superproxy.io:22225'}


response = requests.get('https://www.youtube.com/', proxies=proxies_dict)
