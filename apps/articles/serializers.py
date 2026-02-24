from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ('id', 'title', 'slug', 'content', 'image', 'author', 'author_name', 'status', 'created_at', 'updated_at', 'published_at')
        read_only_fields = ('author', 'published_at')

    def validate_slug(self, value):
        # Basic slug validation if needed
        return value
