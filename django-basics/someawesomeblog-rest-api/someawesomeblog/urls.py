from django.urls import path, include

urlpatterns = [
    path('auth/', include('userauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
