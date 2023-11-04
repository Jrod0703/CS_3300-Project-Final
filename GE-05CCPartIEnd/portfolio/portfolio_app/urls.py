from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # index as the homepage
    path('hours-of-operation/', views.hours_of_operation, name='hours_of_operation'),
    
    # Updating notebook-related URLs to use class-based views
    path('notebooks/', views.NotebookListView.as_view(), name='notebook_list'),
    path('notebooks/<int:pk>/', views.NotebookDetailView.as_view(), name='notebook_detail'),

    # Add URL patterns for updating and deleting rounds, and for the golfer, notebook, and round list and detail views
    path('round/add/<int:notebook_id>/', views.add_round, name='add_round'),
    path('rounds/<int:pk>/delete/', views.delete_round, name='delete_round'),
    path('rounds/<int:pk>/update/', views.update_round, name='update_round'),
    path('notebooks/<int:pk>/update/', views.update_notebook, name='update_notebook'),
    #urls patterns for getting the rounds
    path('golfers/', views.GolferListView.as_view(), name='golfer_list'),
    path('golfers/<int:pk>/', views.GolferDetailView.as_view(), name='golfer_detail'),
    path('rounds/', views.GolfRoundListView.as_view(), name='round_list'),
    path('rounds/<int:pk>/', views.GolfRoundDetailView.as_view(), name='round_detail'),
    #urls patterns for adding/deleting 
    path('add_golfer/', views.add_golfer, name='add_golfer'),
    path('delete_golfer/', views.delete_golfer, name='delete_golfer')
]

