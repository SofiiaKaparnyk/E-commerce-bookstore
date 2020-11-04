from django.contrib.auth.models import User
from django.db import models

RATE_CHOICE = [(r, r) for r in range(1, 6)]


class Owner(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(to='auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=25)
    region = models.CharField(max_length=25)
    street = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return f'{self.user.username}'
