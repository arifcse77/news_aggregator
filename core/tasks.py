from celery import shared_task
from django.utils import timezone
from .models import NewsSource, Article
from .services.feed_parser import FeedParser
from .services.topic_extractor import TopicExtractor


@shared_task
def fetch_and_process_feeds():
    """Celery task to fetch and process all active feeds"""
    topic_extractor = TopicExtractor()
    sources = NewsSource.objects.filter(is_active=True)
    
    for source in sources:
        try:
            articles = FeedParser.fetch_feed(source)
            
            for article_data in articles:
                # Extract topics and entities
                text = f"{article_data['title']} {article_data['description']}"
                topics = topic_extractor.extract_topics(text)
                entities = topic_extractor.extract_entities(text)
                
                # Create or update article
                Article.objects.update_or_create(
                    url=article_data['url'],
                    defaults={
                        'source': source,
                        'title': article_data['title'],
                        'description': article_data['description'],
                        'publication_date': article_data['publication_date'],
                        'topics': topics,
                        'persons': entities['persons'],
                        'organizations': entities['organizations'],
                        'locations': entities['locations']
                    }
                )
            
            # Update last_fetched timestamp
            source.last_fetched = timezone.now()
            source.save()
            
        except Exception as e:
            print(f"Error processing source {source.name}: {e}")