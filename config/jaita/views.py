from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, TemplateView
from django.shortcuts import render
from .forms import LoginForm, AppointmentForm, VitalsForm
from .models import Appointment,Vitals, CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'registrations/signup.html'
    success_url = reverse_lazy('login')
    default_group_name = 'Patient'  # Set the default group name

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        group_name = self.request.POST.get('group_name', self.default_group_name)
        group, created = Group.objects.get_or_create(name=group_name)
        user = self.object
        user.user_permissions.set(group.permissions.all())
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
        

class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context['dashboard'] = 'admin'
        elif user.groups.filter(name='Doctor').exists():
            context['dashboard'] = 'doctor'
        elif user.groups.filter(name='Nurse').exists():
            context['dashboard'] = 'nurse'
        else:
            context['dashboard'] = 'patient'
        return context

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm  # Assuming you have defined an AppointmentForm
    template_name = 'appointment/create.html'
    success_url = reverse_lazy('home')
    default_group_name = 'Patient'  # Set the default group name

    def form_valid(self, form):
        # Assign the user to a group if not already assigned
        group_name = self.default_group_name
        group, created = Group.objects.get_or_create(name=group_name)
        if not self.request.user.groups.filter(name=group_name).exists():
            self.request.user.groups.add(group)
        
        # Assign the user to the appointment
        form.instance.patient = self.request.user.patient
        
        return super().form_valid(form)
    
class VitalsCreateView(LoginRequiredMixin, CreateView):
    model = Vitals
    form_class = VitalsForm
    template_name = 'vitals/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)