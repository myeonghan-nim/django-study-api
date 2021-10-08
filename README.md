# Study: API

## RESTful API

```bash
$ pip install djangorestframework drf-yasg
```

- settings.py

```python
INSTALLED_APPS = [
   'rest_framework',
   'drf_yasg',
]
```

- urls.py

```python
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
        title='Music API',
        default_version='v1',
        description='Test for REST',
        license=openapi.License(name='BSD License'),
   ),
)

urlpatterns = [
    path('api/v1/', include('music.urls')),
    path('redoc/', schema_view.with_ui('redoc')),
    path('swagger/', schema_view.with_ui('swagger')),
]
```

- serializers.py

```python
from rest_framework import serializers

from .models import Music, Artist, Comment


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist_id', ]


class ArtistDetailSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(source='music_set', many=True)
    musics_count = serializers.IntegerField(source='music_set.count')

    class Meta:
        model = Artist
        fields = ['id', 'name', 'musics', 'musics_count', ]
```

- views.py

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import MusicSerializer, CommentSerializer


@api_view(['GET'])
def music_list(request):
    serializer = MusicSerializer(Music.objects.all(), many=True)
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
        return Response({'status': 204})
```
