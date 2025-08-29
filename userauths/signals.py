from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import User
from userauths.models import User
from djoser import signals
from .tasks import send_activation_email_task


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(signals.user_registered)
def send_activation_email(sender, user, request, **kwargs):
    send_activation_email_task.delay(user.id)