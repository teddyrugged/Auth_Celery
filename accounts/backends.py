# accounts/backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.utils import timezone
from django.db import models


class CaseInsensitiveAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        # Check if account is locked in Redis
        if cache.get(f'account_lock:{username}'):
            return None
            
        try:
            user = UserModel.objects.get(
                models.Q(username__iexact=username) | 
                models.Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
            
        # Check password and lockout status
        if user.check_password(password):
            if user.is_locked and user.locked_until > timezone.now():
                return None
            return user
            
        # Increment failed attempts
        attempts = cache.incr(f'login_attempts:{username}')
        if attempts >= 3:
            user.lock_account()
            cache.set(f'account_lock:{username}', 'locked', timeout=900)
        return None