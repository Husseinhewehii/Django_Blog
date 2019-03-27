from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import Profile

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
	""" receiver receives the signal with arguments when attempts to create profile"""
	""" arguments fill the create_file function's paramters"""
	""" profile is created for user who is the (instance) argument"""
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
	""" save profile to user who is the (instance) argument """
	instance.profile.save()
