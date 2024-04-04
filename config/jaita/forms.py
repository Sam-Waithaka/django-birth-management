from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Appointment, Vitals

class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(help_text='Format: YYYY-MM-DD')
    contact_number = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'contact_number', 'address')

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

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']  # Customize fields as needed
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        # Example: Check if the chosen doctor is available at the selected time
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise forms.ValidationError('The selected doctor is not available at the chosen time. Please select another time.')

class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        fields = ['blood_pressure_systolic', 'blood_pressure_diastolic', 'weight', 'temperature']  # Customize fields as needed
