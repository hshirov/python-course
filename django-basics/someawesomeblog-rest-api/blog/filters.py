from django.db.models import Count, Q
import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    hashtag = django_filters.CharFilter(field_name='hashtags__name', lookup_expr='icontains')
    hot = django_filters.BooleanFilter(label='Hot', method='filter_hot')

    def filter_hot(self, queryset, name, value):
        if value:
            posts = queryset.annotate(
                thumbs_up_count=Count('reactions', filter=Q(reactions__reaction_type='thumbs_up')),
                comments_count=Count('comments')
            ).filter(thumbs_up_count__gte=5, comments_count__gte=2)
            return posts

        return queryset

    class Meta:
        model = Post
        fields = ['hashtag', 'hot']


class PostSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    hashtags = django_filters.CharFilter(label='Hashtags', method='filter_hashtags')

    def filter_hashtags(self, queryset, name, hashtags):
        if hashtags:
            tags = hashtags.split(',')
            query = Q()
            for tag in tags:
                query |= Q(hashtags__name__icontains=tag.strip())
            queryset = queryset.filter(query)

        return queryset
    
    class Meta:
        model = Post
        fields = ['title', 'hashtags']
