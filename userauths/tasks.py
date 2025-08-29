# app/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()

@shared_task
def send_activation_email_task(user_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.is_active:
            # Build activation link
            uid = user.pk
            token = user.activation_token if hasattr(user, 'activation_token') else None
            activation_path = settings.DJOSER.get('ACTIVATION_URL', 'auth/activation/{uid}/{token}')
            activation_link = f"{settings.SITE_URL}/{activation_path.format(uid=uid, token=token)}"

            # Prepare email
            subject = f"Activate your {settings.SITE_NAME} account"
            message = render_to_string("emails/activation_email.html", {
                "user": user,
                "activation_link": activation_link
            })

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
    except User.DoesNotExist:
        pass