import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# Initialize logger
logger = logging.getLogger('BlogApi')
User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser named 'admin' with a predefined password"

    def handle(self, *args, **kwargs):
        username = "admin"
        password = "1234"
        email = "admin@example.com"

        # Check if the superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f"Superuser '{username}' already exists."))
            return

        try:
            # Create the superuser
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email
            )
            success_message = f"Superuser '{username}' created successfully with password '{password}'."
            logger.info(success_message)
            self.stdout.write(self.style.SUCCESS(success_message))
        except Exception as e:
            error_message = f"Error creating superuser '{username}': {str(e)}"
            logger.error(error_message)
            self.stderr.write(self.style.ERROR(error_message))
