from django.db.models import Count, Q
import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    hashtag = django_filters.CharFilter(field_name='hashtags__name', lookup_expr='icontains')
    hot = django_filters.BooleanFilter(label='hot', method='filter_hot')

    def filter_hot(self, queryset, name, value):
        if value:
            posts = queryset.annotate(
                thumbs_up_count=Count('reactions', filter=Q(reactions__reaction_type='thumbs_up')),
                comments_count=Count('comments')
            ).filter(thumbs_up_count__gte=5, comments_count__gte=2)
            return posts
        return queryset.all()

    class Meta:
        model = Post
        fields = ['hashtag', 'hot']
