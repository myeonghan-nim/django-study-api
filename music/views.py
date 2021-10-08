from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Music, Artist, Comment
from .serializers import MusicSerializer, ArtistSerializer, ArtistDetailSerializer, CommentSerializer


@api_view(['GET'])
def music_list(request):
    serializer = MusicSerializer(Music.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def music_detail(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    serializer = MusicSerializer(music)
    return Response(serializer.data)


@api_view(['GET'])
def artist_list(request):
    serializer = ArtistSerializer(Artist.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    serializer = ArtistDetailSerializer(artist)
    return Response(serializer.data)


@api_view(['POST'])
def comment_create(request, music_id):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(music_id=music_id)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        comment.delete()
        return Response({'status': 200})
