from django.urls import path
from .views import SignupView, home

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', home, name='home'),
]
