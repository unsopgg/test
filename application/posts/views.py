from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .permissions import IsPostAuthor
from .serializer import *
from .models import SomePosts, Saved


class PostFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(field_name='author_id')

    class Meta:
        model = SomePosts
        fields = ['author_id', ]


#CRUD for posts
class PostListView(generics.ListAPIView):
    queryset = SomePosts.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_class = PostFilter
    search_fields = ['title', ]

    def get_serializer_context(self):
        return {'request': self.request}


class PostCreateView(generics.CreateAPIView):
    queryset = SomePosts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]


class PostUpdateView(generics.UpdateAPIView):
    queryset = SomePosts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]


class PostDeleteView(generics.DestroyAPIView):
    queryset = SomePosts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]


class PostViewSet(viewsets.ModelViewSet):
    queryset = SomePosts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'saved':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsPostAuthor, ]
        return [permissions() for permissions in permissions]


    @action(detail=True, methods=['POST'])
    def saved(self, requests, *args, **kwargs):
        post = self.get_object()
        saved_obj, _ = Saved.objects.get_or_create(post=post, user=requests.user)
        saved_obj.saved = not saved_obj.saved
        saved_obj.save()
        status = 'Сохранено в избранные'
        if not saved_obj.saved:
            status = 'Удалено из избранных'
        return Response({'status': status})

    def get_serializer_context(self):
        return {'request': self.request}

class SavedView(generics.ListAPIView):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer

class PostDetailView(generics.RetrieveAPIView):
    queryset = SomePosts.objects.all()
    serializer_class = PostDetailSerializer