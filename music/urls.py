from django.urls import path

from . import views

app_name = 'music'

urlpatterns = [
    path('music/', views.music_list, name='music_list'),
    path('music/<int:music_id>/', views.music_detail, name='music_detail'),

    path('artist/', views.artist_list),
    path('artist/<int:artist_id>/', views.artist_detail),
    path('music/<int:music_id>/comment/', views.comment_create),
    path('comment/<int:comment_id>/', views.comment_detail),
]
