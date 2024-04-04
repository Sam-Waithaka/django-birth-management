from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

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
    


