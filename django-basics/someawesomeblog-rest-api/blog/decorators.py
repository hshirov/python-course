from functools import wraps
from django.db.models import QuerySet
from rest_framework.response import Response

def paginate(serializerClass=None):
    def decorator(func):
        @wraps(func)
        def wrapped_func(self, *args, **kwargs):
            queryset = func(self, *args, **kwargs)
            assert isinstance(queryset, (list, QuerySet)), "apply_pagination expects a List or a QuerySet"

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = serializerClass(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = serializerClass(queryset, many=True)
            return Response(serializer.data)

        return wrapped_func
    
    return decorator
