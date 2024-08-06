from django.urls import path
from .views import AuthRootView, CreateUserView, LoginView

urlpatterns = [
    path('', AuthRootView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', CreateUserView.as_view(), name='signup'),
]