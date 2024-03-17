from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATUS = (
        ('Direktor', 'Direktor'),
        ('Royxatchi', 'Ro\'yxatchi'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='Royxatchi')

    def __str__(self):
        return self.username


class Bemor(models.Model):
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    dad_name = models.CharField(max_length=60, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}/{self.last_name}'
