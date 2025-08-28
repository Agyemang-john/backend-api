from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import User
from .models import Profile
from userauths.models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        # Try to fetch Google profile image
        try:
            social_user = instance.social_auth.get(provider='google-oauth2')
            picture_url = social_user.extra_data.get('picture')
            if picture_url:
                profile.profile_image = picture_url
                profile.save()
        except Exception as e:
            print("Social image not found or failed:", e)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()