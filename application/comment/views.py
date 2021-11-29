from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CommentSerializer
from .permissions import IsCommentAuthor
from .models import Comment, Like


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsCommentAuthor, ]
        return [permissions() for permissions in permissions]



    @action(detail=True, methods=['POST'])
    def like(self, requests, *args, **kwargs):
        comment = self.get_object()
        like_obj, _ = Like.objects.get_or_create(comment=comment, user=requests.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'Postavil layk'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})

    def get_serializer_context(self):
        return {'request': self.request}