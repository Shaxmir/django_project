"""
URL configuration for sait_one project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from block import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('about/', views.about),
    path('catalog/', views.сatalog),
    path('contact/', views.contact),
    path('task/', views.task),
    path('task/handle/', views.handle),
    path('task/create/', views.create),
    path('task/<int:id>/edit/', views.edit),
    path('task/<int:id>/delete/', views.delete),
    path('books/', views.books),
    path('books/<int:id>/', views.books),
    path('books/add_book/', views.add_book),
    path('books/<str:author>/author/', views.author),
    path('books/<int:id>/book_edit/', views.book_edit),
    path('books/<int:id>/sell/', views.sell),
    path('post/', views.post,  name='post'),
    path('post/<int:id>/', views.post,  name='post_id'),
    path('post/create_post/', views.create_post, name='post_create'),
    path('post/<int:id>/edit_post/', views.edit_post, name='post_edit'),
    path('post/<int:id>/delete_post', views.delete_post, name='post_delete'),
    path('chat/', views.chat, name='chat'),
    path('polls/', views.polls, name='polls'),
    path('polls/<int:id>/', views.polls, name='poll'),
    path('polls/<int:id>/vote/', views.vote, name='poll_vote'),
]
