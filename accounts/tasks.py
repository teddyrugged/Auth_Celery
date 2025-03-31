# accounts/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
import secrets

@shared_task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    token = secrets.token_urlsafe(32)
    user.verification_token = token
    user.save()
    
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    send_mail(
        'Verify Your Account',
        f'Click to verify: {verification_url}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


    