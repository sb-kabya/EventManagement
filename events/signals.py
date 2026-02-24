from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import RSVP
from django.urls import reverse
from django.conf import settings


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = 'dummy-token-for-console' 
        activation_link = f"http://127.0.0.1:8000/events/activate/{instance.pk}/{token}/"
        send_mail(
            'Activate your account',
            f'Click here to activate: {activation_link}',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True
        )


@receiver(post_save, sender=RSVP)
def send_rsvp_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f'Confirmation for {instance.event.name}',
            f'Hi {instance.user.username}, you have registered for {instance.event.name}',
            settings.EMAIL_HOST_USER,
            [instance.user.email],
            fail_silently=True
        )