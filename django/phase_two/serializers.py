from rest_framework import serializers
from .models import Item, Comment

class ItemSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'id', 'categories', 'user', 'created_at', 'username']

    def get_username(self, obj):
        return obj.user.username

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['item', 'user', 'created_at', 'rating', 'comment']