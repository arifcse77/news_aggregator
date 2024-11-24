from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sources', views.NewsSourceViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('api/', include(router.urls)),
]