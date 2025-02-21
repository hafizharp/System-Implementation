from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search_github_links/', views.search_github_links, name='search_github_links'),
    path('deploy_to_vercel/', views.deploy_to_vercel, name='deploy_to_vercel'),
]
