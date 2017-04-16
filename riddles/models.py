from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=12)
    level = models.IntegerField(default=1)
    sublevel = models.IntegerField(default=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userdetails.save()


class Answers(models.Model):
    level = models.IntegerField()
    sublevel = models.IntegerField()
    answer = models.CharField(max_length=100)