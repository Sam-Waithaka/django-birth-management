from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, ListView, View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import LoginForm

def home(request):
    return render(request, 'home.html')  # You can change 'home.html' to the appropriate template


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'registrations/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        group_name = self.request.POST.get('group_name')
        group = Group.objects.get(name=group_name)
        user = self.object
        user.groups.add(group)
        user.save()
        return response
    
class LoginView(FormView):
    template_name = 'registrations/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
