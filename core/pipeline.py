from django.contrib.auth import get_user_model

User = get_user_model()

def associate_by_email(strategy, details, backend, uid, user=None, *args, **kwargs):
    if user:
        return {'user': user}
    email = details.get('email')

    if email:
        try:
            user = User.objects.get(email=email)
            return {'user': user} # ✅ LOGIN existing user
        except User.DoesNotExist:
            return None # create new user