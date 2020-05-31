from datetime import datetime
from typing import (List, Dict, Tuple, Set)

from flask import (jsonify, request)
from flask.views import MethodView
from flask_cors import cross_origin

from apps import database
from apps.youtube_scraper.models import (Result, ScraperResultChange)
from source.scrapers import (YoutubeScraper, spotify_api)
from source.loggers import logger


class YouTubeCrawler(MethodView):
    @cross_origin()
    def get(self):
        """Handle with word search in youtube"""
        logger.info(f'received request on {request.url}')
        # Check whether requested arguments are correct
        check_status, data = self.check_args
        if not check_status:
            return data, 406
        # Create crawler instance and run crawling
        scraper = YoutubeScraper(**data)
        meta_results: List[dict] = scraper.run()
        # If no results return message
        if not meta_results:
            logger.info(f'no results from youtube on word: {data["query_word"]}')

            return jsonify({'data': []})
        # Add spotify data and create database objects
        # Results to response to the user request
        results: List[Result] = list()
        # Cache artist data in session
        artists: Dict[str, dict] = dict()
        # Create results and add them into database
        for result_dict in meta_results:
            parser_result = Result.query.filter(Result.youtube_id == result_dict['youtube_id']).first() or Result()
            # Load model from dictionary
            parser_result.from_dict(**result_dict)
            # Get Spotify data or use cached one from session
            artist = artists.get(parser_result.artist_name, {})
            if parser_result.artist_name and not artist.get('checked'):
                logger.info(f'searching artist in spotify with name: {parser_result.artist_name}')

                artist = spotify_api.search_artist(parser_result.artist_name)
                artist['checked'] = True
            # Updated artists cache
            artists[parser_result.artist_name] = artist
            if artist.get('id'):
                parser_result.is_on_spotify = True
                parser_result.total_followers = artist['followers']['total']
            # Update results for return
            results.append(parser_result)

        # Insert results into database
        database.session.add_all(results)
        database.session.commit()
        results.sort(key=lambda x: x.views, reverse=True)

        return jsonify({'data': [result.serialize for result in results]})

    @property
    def check_args(self):
        # Get request arguments
        max_views: str = request.args.get('max_views', '')
        min_views: str = request.args.get('min_views', '')
        search_word: str = request.args.get('query_word', '')
        # Restrict view num only integers
        if not max_views.isdigit() or not min_views.isdigit() or (int(min_views) >= int(max_views)):
            logger.error(
                f'{request.url} error in either max or min views: they must be integers {min_views}, {max_views}')

            return False, {'data': 'error in either max or min views: they must be integers, or min >= max'}
        # Restrict min length query words
        if not search_word or len(search_word) < 3:
            logger.error(f'{request.url} query word to short: {search_word}')

            return False, {'data': 'query word too short (required min 3 symbols)'}

        return True, {'search_word': search_word, 'min_views': int(min_views), 'max_views': int(max_views)}

    @staticmethod
    def youtube_meta_handler(meta_results: List[dict]) -> Tuple[List[Result], Set[Result]]:
        """Search on spotify and add metadata to existing results"""
        # Results to response to the user request
        results: List[Result] = list()
        new_results: List[Result] = list()
        # Cache artist data in session
        artists: Dict[str, dict] = dict()
        # Create results and add them into database
        for result_dict in meta_results:
            parser_result = Result()
            # Load model from dictionary
            parser_result.from_dict(**result_dict)
            # Get Spotify data or use cached one from session
            artist = artists.get(parser_result.artist_name, {})
            if parser_result.artist_name and not artist.get('checked'):
                logger.info(f'searching artist in spotify with name: {parser_result.artist_name}')

                artist = spotify_api.search_artist(parser_result.artist_name)
                artist['checked'] = True
            # Updated artists cache
            artists[parser_result.artist_name] = artist
            if artist.get('id'):
                parser_result.is_on_spotify = True
                parser_result.total_followers = artist['followers']['total']
            # Update results for return
            results.append(parser_result)
            if result_dict.get('existing'):
                continue

            new_results.append(parser_result)
        # Get only unique results for database

        return results, set(new_results)

    @cross_origin()
    def post(self):
        logger.info(f'received request on {request.url} with data {request.json}')
        result = Result.query.filter(Result.youtube_id == request.json.get('youtube_id')).first()
        if not result:
            return jsonify({'data': 'ok'})

        new_artist_name = request.json.get('artist_name')
        # Log field changes in database
        result_change = ScraperResultChange(field='artist_name', result_id=result.id)
        result_change.old_value = result.artist_name
        result_change.new_value = new_artist_name
        # Update result
        result.artist_name = new_artist_name
        result.last_change_date = datetime.now()
        # Update spotify information for new artist
        artist = spotify_api.search_artist(new_artist_name)
        # Updated artist
        if artist.get('id'):
            result.is_on_spotify = True
            result.total_followers = artist['followers']['total']

        database.session.add_all([result, result_change])
        database.session.commit()

        return jsonify({'data': result.serialize})
