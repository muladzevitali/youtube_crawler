from time import time

import requests

counter = 1
headers = {
    'accept-language': 'en-US,en;q=0.9,ka-GE;q=0.8,ka;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',
}
global_start = time()
while True:
    request_start = time()
    response = requests.get('https://www.youtube.com/watch?v=xECQJ62vCJU', headers=headers)
    request_stop = time()
    print(counter, '*' * 10, response.status_code, 'request_time:', request_stop - request_start, 'global time:',
          time() - global_start)
    counter += 1
    if response.status_code != 200:
        break
