
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    
    def lock_account(self):
        
        self.is_locked = True
        self.save(update_fields=['is_locked'])
    
    def unlock_account(self):
        self.is_locked = False
        self.failed_login_attempts = 0
        self.save(update_fields=['is_locked', 'failed_login_attempts'])

    def is_account_locked(self) -> bool:
        """
        Returns True if account is locked.
        """
        return self.is_locked
