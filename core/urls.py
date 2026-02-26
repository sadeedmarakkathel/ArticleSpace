"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.articles.views import (
    ArticleListView, ArticleDetailView, DashboardView, 
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView, publish_article
)

urlpatterns = [
    # Consumer Web UI
    path('', ArticleListView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('articles/new/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<slug:slug>/publish/', publish_article, name='article_publish_ui'),
    
    # Account Management
    path('accounts/', include('apps.accounts.urls')),
    path('admin/', admin.site.urls),
    
    # REST API Integration Layer (Internal/Mobile/Developers)
    path('api/v1/', include('apps.articles.urls')),
    path('api/v1/auth/', include('apps.accounts.urls')),
]

from django.urls import re_path
from django.views.static import serve

# Serve media files in both development and production (for Render deployment)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
