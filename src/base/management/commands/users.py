import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

# Initialize logger
logger = logging.getLogger('BlogApi')
User = get_user_model()
faker = Faker()


class Command(BaseCommand):
    help = "Generate 10 users for testing purposes"

    def handle(self, *args, **kwargs):
        try:
            for _ in range(10):
                User.objects.create_user(
                    username=faker.unique.user_name(),
                    email=faker.unique.email(),
                    password=faker.password()
                )
            logger.info("10 users created successfully.")
            self.stdout.write(self.style.SUCCESS(
                "10 users created successfully."))
        except Exception as e:
            logger.error(f"Error generating users: {str(e)}")
            self.stdout.write(self.style.ERROR(
                f"Failed to create users: {str(e)}"))
