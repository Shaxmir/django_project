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
from django.urls import path
from block import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index),
    path('about/', views.about),
    path('catalog/', views.сatalog),
    path('contact/', views.contact),
    path('task/', views.task),
    path('task/handle/', views.handle),
    path('task/create/', views.create),
    path('task/<int:id>/edit/', views.edit),
    path('task/<int:id>/delete/', views.delete),

]
