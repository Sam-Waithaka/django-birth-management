from django.urls import path
from .views import SignupView, LoginView, HomeView, LogoutView, AppointmentCreateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('appointment/', AppointmentCreateView.as_view(), name='appointment'),
    path('', HomeView.as_view(), name='home'),
]
