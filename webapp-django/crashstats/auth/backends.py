from django.conf import settings
from django_browserid.auth import BrowserIDBackend

class SocorroBrowserIDBackend(BrowserIDBackend):
    def create_user(*args, **kwargs):
        auto_superuser_domain = getattr(settings, 'AUTO_SUPERUSER_USERS_IN_DOMAIN', None)

        user = super().create_user(*args, **kwargs)
        if not auto_superuser_domain:
            return user

        if not user or not user.is_active:
            return user

        if isinstance(user.email, basestring) and user.email.endswith('@%s' % auto_superuser_domain):
            user.is_superuser = True
            user.save()

        return user
