from django.db import models
from django.contrib.auth.models import User
from .utils import extract_hashtags


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text_content = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_reaction_count(self, reaction_type):
        return self.reactions.filter(reaction_type=reaction_type).count()
    
    def get_comment_count(self):
        return self.comments.count()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        hashtags = {tag.lower() for tag in extract_hashtags(self.text_content)}
        existing_hashtags = Hashtag.objects.filter(name__in=hashtags)
        existing_hashtag_names = existing_hashtags.values_list('name', flat=True)

        new_hashtags = [Hashtag(name=tag) for tag in hashtags if tag not in existing_hashtag_names]
        Hashtag.objects.bulk_create(new_hashtags)

        all_hashtags = list(existing_hashtags) + new_hashtags
        self.hashtags.set(all_hashtags)


class Comment(models.Model):
    text_content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Reaction(models.Model):
    REACTION_CHOICES = [
        ('thumbs_up', 'Thumbs Up'),
        ('thumbs_down', 'Thumbs Down'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=11, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reaction_type} by {self.author.username} on {self.post.title}'
