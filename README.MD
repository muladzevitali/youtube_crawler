# Youtube Crawler
> Docker compose for youtube crawler backend and frontend

Docker compose with python flask, postgres and react containers. 
Flask runs on the 5000 port. React on 3000

### Available endpoints of api
* /rest/v1/youtube/crawl?query_word=<search_word>&max_views=1000000&min_views=100000

### PM2 start script
```bash
pm2 start node_modules/react-scripts/scripts/start.js --name youtube_scraper
```
## Usage
* Before running container change the frontend/.env.development environment variable for the backend url accordingly
* run
```bash
docker-compose build
docker-compose up
```