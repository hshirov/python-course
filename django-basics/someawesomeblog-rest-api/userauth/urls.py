from django.urls import path
from rest_framework.authtoken import views
from .views import AuthRootView, CreateUserView, LoginView

urlpatterns = [
    path('', AuthRootView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('token/', views.obtain_auth_token)
]