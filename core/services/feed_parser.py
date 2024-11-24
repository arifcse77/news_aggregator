import feedparser
from datetime import datetime
from dateutil import parser as date_parser
import logging
from urllib.parse import urlparse
import requests

logger = logging.getLogger(__name__)

class FeedParser:
    @staticmethod
    def validate_url(url):
        """Validate URL format and accessibility"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def parse_date(date_str):
        """Parse various date formats to datetime"""
        try:
            return date_parser.parse(date_str)
        except:
            return datetime.utcnow()


    @staticmethod
    def fetch_feed(source):
        """Fetch and parse a single feed"""
        try:
            if not FeedParser.validate_url(source.url):
                raise ValueError(f"Invalid URL: {source.url}")

            feed = feedparser.parse(source.url)
            articles = []

            for entry in feed.entries:
                article = {
                    'title': entry.get('title', ''),
                    'description': entry.get('description', ''),
                    'url': entry.get('link', ''),
                    'publication_date': FeedParser.parse_date(entry.get('published', '')),
                    'source': source,
                }
                articles.append(article)

            return articles
        except Exception as e:
            logger.error(f"Error fetching feed {source.name}: {e}")
            return []