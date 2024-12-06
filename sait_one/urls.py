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
from block.views import BasePage, ObjectDetailView, CreatedMaster, EditMaster, DeleteMaster

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BasePage.as_view(), name='page'),
    path('<str:page>/', BasePage.as_view(), name='pages'),
    path('<str:page>/filter', BasePage.as_view(), name='filter'),
    path('<str:page>/handle/', BasePage.as_view(), name='task_handle'),
    path('<str:page>/create/', CreatedMaster.as_view(), name='task_create'),
    path('<str:page>/<int:id>/edit/', EditMaster.as_view(), name='taks_edit'),
    path('<str:page>/<int:id>/delete/', DeleteMaster.as_view(), name='task_del'),
    path('<str:page>/<int:id>/', ObjectDetailView.as_view(), name='books'),
    path('<str:page>/add_book/', BasePage.as_view(), name='book_add'),
    path('<str:page>/<str:author>/author/', BasePage.as_view(), name='filet_book_aut'),
    path('<str:page>/<int:id>/book_edit/', BasePage.as_view(), name='book_edit'),
    path('<str:page>/<int:id>/sell/', BasePage.as_view(), name='book_sell'),
    path('<str:page>/create_post/', BasePage.as_view(), name='post_create'),
    path('<str:page>/<int:id>/edit_post/', BasePage.as_view(), name='post_edit'),
    path('<str:page>/<int:id>/delete_post', BasePage.as_view(), name='post_delete'),
    path('<str:page>/poll/<int:id>/', BasePage.as_view(), name='poll'),
    path('<str:page>/poll/<int:id>/vote/', BasePage.as_view(), name='poll_vote'),
]
