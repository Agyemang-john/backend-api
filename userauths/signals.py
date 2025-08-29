from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import User
from userauths.models import User
from djoser import signals


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
