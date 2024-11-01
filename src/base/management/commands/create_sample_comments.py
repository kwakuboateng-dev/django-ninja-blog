import logging
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from base.models import Post, Comment
from faker import Faker

# Initialize logger
logger = logging.getLogger('BlogApi')
User = get_user_model()
faker = Faker()


class Command(BaseCommand):
    help = "Generate a set number of sample comments for testing purposes"

    def add_arguments(self, parser):
        # Adding argument for the number of sample comments to create
        parser.add_argument(
            'count',
            type=int,
            nargs='?',
            help='Number of sample comments to create'
        )

    def handle(self, *args, **kwargs):
        count = kwargs.get('count')

        # Validate the 'count' argument
        if count is None or count <= 0:
            error_message = "The 'count' argument is required and must be a positive integer."
            logger.error(error_message)
            self.stderr.write(self.style.ERROR(error_message))
            return

        # Get all users to use as authors and all posts to comment on
        authors = User.objects.all()
        posts = Post.objects.all()

        if not authors.exists() or not posts.exists():
            error_message = "No users or posts found. Create users and posts first."
            logger.error(error_message)
            self.stderr.write(self.style.ERROR(error_message))
            return

        try:
            # Create the specified number of sample comments
            for _ in range(count):
                # Randomly select an author and a post
                author = faker.random_element(elements=authors)
                post = faker.random_element(elements=posts)

                Comment.objects.create(
                    id=uuid.uuid4(),
                    post=post,
                    author=author,
                    text=faker.paragraph()
                )

            success_message = f"{count} sample comments created successfully."
            logger.info(success_message)
            self.stdout.write(self.style.SUCCESS(success_message))

        except Exception as e:
            error_message = f"Error generating sample comments: {str(e)}"
            logger.error(error_message)
            self.stderr.write(self.style.ERROR(
                f"Failed to create sample comments: {str(e)}"))
