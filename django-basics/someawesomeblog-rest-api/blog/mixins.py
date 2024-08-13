from rest_framework import viewsets, mixins


class SaveAuthorMixin:
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListDestroyViewset(mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    pass


class ListCreateDestroyViewset(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass
