from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Products model without timestamps
class Products(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# Custom user model
class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.email

@receiver(post_save, sender=AuthUser)
def create_auth_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
