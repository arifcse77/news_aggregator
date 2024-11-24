from rest_framework import serializers
from .models import NewsSource, Article

class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSource
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'source_name', 'title', 'description', 'url',
            'publication_date', 'topics', 'persons', 'organizations',
            'locations', 'created_at'
        ]
