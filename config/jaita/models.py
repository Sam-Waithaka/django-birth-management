from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users',  # Update related_name to avoid conflicts
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users_permissions',  # Update related_name to avoid conflicts
        related_query_name='user',
        help_text=_('Specific permissions for this user.'),
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new user
            self.is_patient = True  # Assign the role of patient by default
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    # Additional patient information
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    allergies = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    # Additional doctor information
    specialization = models.CharField(max_length=50)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Doctor)"

class Nurse(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    # Additional nurse information
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Nurse)"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='Scheduled')
    notes = models.TextField(blank=True)
    reason = models.TextField()

    class Meta:
        unique_together = ['date', 'time']  # Unique constraint to prevent double booking

    def __str__(self):
        return f"{self.patient} - Appointment with Dr. {self.doctor.user.last_name} on {self.date}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # Medical record details
    due_date = models.DateField()
    delivery_date = models.DateField(blank=True, null=True)
    delivery_details = models.TextField(blank=True)
    week_of_pregnancy = models.PositiveSmallIntegerField(blank=True, null=True)
    blood_pressure_systolic = models.PositiveSmallIntegerField(blank=True, null=True)
    blood_pressure_diastolic = models.PositiveSmallIntegerField(blank=True, null=True)
    weight_measurement = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ultrasound_report = models.FileField(upload_to='ultrasound_reports/', blank=True)
    prescriptions = models.TextField(blank=True)

    def __str__(self):
        return f"Medical Record for {self.patient.user.last_name}"
    
class Vitals(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blood_pressure_systolic = models.PositiveSmallIntegerField()
    blood_pressure_diastolic = models.PositiveSmallIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Vitals for {self.patient.user.last_name}"

2 / 2


