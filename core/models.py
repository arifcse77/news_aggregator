from django.db import models
from django.contrib.postgres.fields import ArrayField

class NewsSource(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField()
    url = models.URLField(unique=True)
    publication_date = models.DateTimeField()
    topics = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    persons = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    organizations = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    locations = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_date']
        indexes = [
            models.Index(fields=['publication_date']),
            models.Index(fields=['url']),
        ]

    def __str__(self):
        return self.title
