from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NewsSource, Article
from .serializers import NewsSourceSerializer, ArticleSerializer
from .tasks import fetch_and_process_feeds
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

class NewsSourceViewSet(viewsets.ModelViewSet):
    queryset = NewsSource.objects.all()
    serializer_class = NewsSourceSerializer
    
    @action(detail=False, methods=['post'])
    def fetch_all(self, request):
        """Trigger manual feed fetch"""
        fetch_and_process_feeds.delay()
        return Response({'status': 'Feed fetch initiated'})

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source', 'topics', 'persons', 'organizations', 'locations']
    search_fields = ['title', 'description']
    ordering_fields = ['publication_date', 'created_at']


class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.select_related('source').all()[:20]
        context['sources'] = NewsSource.objects.all()
        return context