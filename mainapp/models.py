from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import create_shortened_url

# Create your models here.

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)






class shortcut(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    url = models.URLField()
    shortlink = models.CharField(unique=True,blank=True,max_length=100)
    description = models.TextField()
    tags = models.TextField(blank=True)

    
    def __str__(self):
         return f'{self.url} to {self.shortlink}'

    def save(self, *args, **kwargs):
        if not self.shortlink:
            self.shortlink = create_shortened_url(self)

        super().save(*args, **kwargs)
    



