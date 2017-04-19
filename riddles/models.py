import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings

class UserDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile = models.CharField(max_length=12)
	level = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	rank = models.IntegerField(default=0)

	def last_seen(self):
		return cache.get('status_%s' % self.user.username)

	def online(self):
		if self.last_seen():
			now = datetime.datetime.now()
			if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
				return False
			else:
				return True
		else:
			return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserDetails.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userdetails.save()


class Answers(models.Model):
	level = models.DecimalField(max_digits=3, decimal_places=1)
	answer = models.CharField(max_length=100)