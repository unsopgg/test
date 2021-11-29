from rest_framework import serializers
from .models import SomePosts, Saved
from ..comment.serializers import CommentSerializer


class SavedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Saved
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomePosts
        fields = ('id', 'title', 'image', 'post',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user.id
        post = SomePosts.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_rating = [i.rating for i in instance.comment.all()]
        if len(total_rating) > 0:
            representation['total_rating'] = sum(total_rating) / len(total_rating)
        representation['image'] = PostImageSerializer(SomePosts.objects.filter(post=instance.id), many=True, context=self.context).data
        return representation


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomePosts
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
                print(url)
        else:
            url = ''
        return url


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SomePosts
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_rating = [i.rating for i in instance.comment.all()]
        if len(total_rating) > 0:
            representation['total_rating'] = sum(total_rating) / len(total_rating)
        representation['image'] = PostImageSerializer(SomePosts.objects.filter(post=instance.id), many=True,
                                                          context=self.context).data
        representation['comments'] = CommentSerializer(instance.comment.filter(post=instance.id), many=True).data
        return representation