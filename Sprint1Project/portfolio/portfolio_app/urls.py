from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
  
    path('', views.index, name='index'),  # index as the homepage
    path('hours-of-operation/', views.hours_of_operation, name='hours_of_operation'),
    
    # updating notebook-related URLs to use class-based views
    path('notebooks/', views.NotebookListView.as_view(), name='notebook_list'),
    path('notebooks/<int:pk>/', views.NotebookDetailView.as_view(), name='notebook_detail'),

    # urls patterns for updating and deleting rounds, and for the golfer, notebook, and round list and detail views
    path('round/add/<int:notebook_id>/', views.add_round, name='add_round'),
    path('rounds/<int:pk>/delete/', views.delete_round, name='delete_round'),
    path('rounds/<int:pk>/update/', views.update_round, name='update_round'),
    path('notebooks/<int:pk>/update/', views.update_notebook, name='update_notebook'),
    #urls patterns for getting the rounds
   
    #urls patterns for adding/deleting 
    path('add_golfer/', views.add_golfer, name='add_golfer'),
    path('delete_golfer/', views.delete_golfer, name='delete_golfer'),

    #  patterns for register, login, logout
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Add a new URL pattern for uploading files to a notebook   
    path('notebooks/<int:pk>/upload/', views.upload_file_to_notebook, name='upload_file_to_notebook'),
    #path to delete media
    path('delete_media/<int:pk>/<str:media_type>/', views.delete_media, name='delete_media')

]

