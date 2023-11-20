from django.db import models


class User(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, help_text='User ID')
    name = models.CharField(max_length=100, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email ID', unique=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Others')))
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    city = models.CharField(max_length=50, verbose_name='City of Residence')
    state = models.CharField(max_length=50, verbose_name='State / Province')
    bio = models.TextField(max_length=300, blank=True, null=True, verbose_name='Bio / Profile headline')
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    last_updated_at = models.DateTimeField(editable=False, auto_now=True)
    is_active = models.BooleanField(default=True)
