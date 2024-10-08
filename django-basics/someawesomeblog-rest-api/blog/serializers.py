from rest_framework import serializers
from .models import Post, Comment, Hashtag, Reaction
from .utils import extract_hashtags

REACTION_TYPES = [c[0] for c in Reaction.REACTION_CHOICES]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    reaction_counts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text_content', 'reaction_counts', 'author', 'created_at']

    def validate(self, data):
        text = data.get('text_content')
        hashtags = {tag.lower() for tag in extract_hashtags(text)}
        if len(hashtags) > 10:
            raise serializers.ValidationError('You can only add 10 hashtags per post.')
        return data

    def get_reaction_counts(self, obj):
        # TODO: Optimize
        reaction_counts = {type: obj.reactions.filter(reaction_type=type).count() for type in REACTION_TYPES}
        return reaction_counts


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'text_content', 'post', 'author', 'created_at']


class HashtagSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'posts']


class ReactionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Reaction
        fields = ['id', 'reaction_type', 'post', 'author', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        post = data.get('post')
        reaction_type = data.get('reaction_type')
        
        if Reaction.objects.filter(author=request.user, post=post, reaction_type=reaction_type).exists():
            raise serializers.ValidationError('A user can only have one reaction per post.')
        return data
