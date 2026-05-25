from django.contrib.auth.models import User
from django.conf import settings
username = settings.ADMIN_USERNAME

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="",
        password=settings.ADMIN_PASSWORD
    )

    print("Superuser created")
else:
    print("Superuser already exists")