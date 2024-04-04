from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django import forms

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        group_name = self.request.POST.get('group_name')
        group = Group.objects.get(name=group_name)
        user = self.object
        user.groups.add(group)
        user.save()
        return response
    

class LoginForm(AuthenticationForm):
    # You can customize the form fields here if needed
    # For example, you might want to add some CSS classes
    # or placeholder texts to the form fields.
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
