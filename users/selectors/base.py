from django.contrib.auth import get_user_model
User = get_user_model()

def fetch_all_users(**kwargs):
    return User.objects.filter(**kwargs)