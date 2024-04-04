from django.urls import path
from .views import SignupView, LoginView, HomeView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
]
