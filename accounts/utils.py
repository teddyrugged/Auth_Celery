# from django.core.cache import cache
# from django.utils import timezone
# from datetime import timedelta

# def check_account_lock(username):
#     return cache.get(f'account_lock:{username}')

# def increment_failed_attempts(username):
#     cache_key = f'login_attempts:{username}'
#     attempts = cache.incr(cache_key)
#     cache.expire(cache_key, timedelta(minutes=30).total_seconds()
#     return attempts