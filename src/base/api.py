import logging
import uuid
from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import Q

from ninja import FilterSchema, Query
from ninja.pagination import paginate, PageNumberPagination
from ninja_extra import api_controller, http_get, http_post, http_delete, http_generic, status, ControllerBase

from .models import Post, Comment
from .schemas import (
    ErrorSchema, PostCreateSchema, PostUpdateSchema, PostDetailSchema,
    CommentCreateSchema, CommentUpdateSchema, CommentDetailSchema, SuccessSchema
)

# Initialize logger
logger = logging.getLogger('BlogApi')

# Get the User model
User = get_user_model()


@api_controller('/posts')
class PostController(ControllerBase):
    """Controller for handling CRUD operations for blog posts."""

    @http_post()
    def create_post(self, request, post: PostCreateSchema):
        """
        Create a new blog post.

        Args:
            request: The request object containing user information.
            post: PostCreateSchema object with the title and content of the post.

        Returns:
            PostDetailSchema: The newly created post details.
        """
        try:
            user = request.user  # Authenticated User instance
            new_post = Post.objects.create(
                id=uuid.uuid4(),
                title=post.title,
                content=post.content,
                author=user
            )
            logger.info(f"Post created by {user.username}: {new_post.id}")
            return PostDetailSchema.from_orm(new_post)
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            return {"error": "Failed to create post."}

    @http_generic('/{uuid:post_id}', methods=['put', 'patch'], response=PostDetailSchema)
    def update_post(self, post_id: uuid.UUID, post: PostUpdateSchema):
        """
        Update an existing blog post.

        Args:
            post_id: The UUID of the post to update.
            post: PostUpdateSchema object with the fields to be updated.

        Returns:
            PostDetailSchema: The updated post details.
        """
        try:
            existing_post = Post.objects.get(id=post_id)
            for attr, value in post.dict(exclude_unset=True).items():
                setattr(existing_post, attr, value)
            existing_post.save()
            logger.info(f"Post updated: {existing_post.id}")
            return PostDetailSchema.from_orm(existing_post)
        except Post.DoesNotExist:
            logger.warning(f"Post with ID {post_id} not found for update.")
            return {"error": "Post not found."}
        except Exception as e:
            logger.error(f"Error updating post {post_id}: {str(e)}")
            return {"error": "Failed to update post."}

    @http_delete('/{uuid:post_id}', response={204: None, 404: ErrorSchema, 500: ErrorSchema})
    def delete_post(self, post_id: uuid.UUID):
        """
        Delete a blog post.

        Args:
            post_id: The UUID of the post to delete.

        Returns:
            HTTP 204 No Content response on successful deletion, or an error response if deletion fails.
        """
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            logger.info(f"Post deleted: {post_id}")
            # 204 No Content: Success message (optional body)
            return self.create_response("Post deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            logger.warning(f"Post with ID {post_id} not found for deletion.")
            # 404 Not Found: Error message
            return self.create_response("Post not found.", status_code=404)
        except Exception as e:
            logger.error(f"Error deleting post {post_id}: {str(e)}")
            # 500 Internal Server Error: Error message
            return self.create_response(f"Failed to delete post. Details: {str(e)}", status_code=500)

    @ http_get("", response=list[PostDetailSchema])
    @ paginate(PageNumberPagination, page_size=10)
    def list_posts(self):
        query = Post.objects.all()
        return [PostDetailSchema.from_orm(post) for post in query]

    @ http_get('/{uuid:post_id}', response=PostDetailSchema)
    def get_post_by_id(self, post_id: uuid.UUID):
        """
        Retrieve details of a specific blog post.

        Args:
            post_id: The UUID of the post to retrieve.

        Returns:
            PostDetailSchema: The details of the requested post.
        """
        try:
            post = Post.objects.get(id=post_id)
            logger.info(f"Post retrieved: {post.id}")
            return PostDetailSchema.from_orm(post)
        except Post.DoesNotExist:
            logger.warning(f"Post with ID {post_id} not found.")
            return {"error": "Post not found."}
        except Exception as e:
            logger.error(f"Error retrieving post {post_id}: {str(e)}")
            return {"error": "Failed to retrieve post."}


@api_controller('/comments')
class CommentController(ControllerBase):
    """Controller for handling CRUD operations for comments on blog posts."""

    @http_post()
    def create_comment(self, request, comment: CommentCreateSchema):
        """
        Create a new comment on a blog post.

        Args:
            request: The request object containing user information.
            comment: CommentCreateSchema object with the post ID and text.

        Returns:
            CommentDetailSchema: The newly created comment details with the author's name.
        """
        try:
            new_comment = Comment.objects.create(
                id=uuid.uuid4(),
                post_id=comment.post,
                author=request.user,  # Use the authenticated user as the author
                text=comment.text
            )
            logger.info(
                f"Comment created: {new_comment.id} for post {comment.post}")
            return CommentDetailSchema.from_orm(new_comment)
        except Exception as e:
            logger.error(f"Error creating comment: {str(e)}")
            return {"error": "Failed to create comment."}

    @http_generic('/{uuid:comment_id}', methods=['put', 'patch'], response=CommentDetailSchema)
    def update_comment(self, comment_id: uuid.UUID, comment: CommentUpdateSchema):
        """
        Update an existing comment.

        Args:
            comment_id: The UUID of the comment to update.
            comment: CommentUpdateSchema object with the text to be updated.

        Returns:
            CommentDetailSchema: The updated comment details.
        """
        try:
            existing_comment = Comment.objects.get(id=comment_id)
            for attr, value in comment.dict(exclude_unset=True).items():
                setattr(existing_comment, attr, value)
            existing_comment.save()
            logger.info(f"Comment updated: {existing_comment.id}")
            return CommentDetailSchema.from_orm(existing_comment)
        except Comment.DoesNotExist:
            logger.warning(
                f"Comment with ID {comment_id} not found for update.")
            return {"error": "Comment not found."}
        except Exception as e:
            logger.error(f"Error updating comment {comment_id}: {str(e)}")
            return {"error": "Failed to update comment."}

    @http_delete('/{uuid:comment_id}', response={204: None, 404: ErrorSchema, 500: ErrorSchema})
    def delete_comment(self, comment_id: uuid.UUID):
        """
        Delete a comment.

        Args:
            comment_id: The UUID of the comment to delete.

        Returns:
            HTTP 204 No Content response on successful deletion, or an error response if deletion fails.
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            logger.info(f"Comment deleted: {comment_id}")
            return self.create_response(None, status_code=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            logger.warning(
                f"Comment with ID {comment_id} not found for deletion.")
            return self.create_response({"error": "Comment not found."}, status_code=404)
        except Exception as e:
            logger.error(f"Error deleting comment {comment_id}: {str(e)}")
            return self.create_response({"error": f"Failed to delete comment. Details: {str(e)}"}, status_code=500)

    @http_get('/post/{uuid:post_id}', response=list[CommentDetailSchema])
    @paginate(PageNumberPagination, page_size=10)
    def get_comments_by_post(self, post_id: uuid.UUID):
        """
        Retrieve all comments for a specific blog post, with pagination.

        Args:
            post_id: The UUID of the post whose comments are to be retrieved.

        Returns:
            List[CommentDetailSchema]: A paginated list of comments for the specified post.
        """
        try:
            comments = Comment.objects.filter(post_id=post_id)
            logger.info(f"Comments requested for post: {post_id}")
            return [CommentDetailSchema.from_orm(comment) for comment in comments]
        except Exception as e:
            logger.error(
                f"Error retrieving comments for post {post_id}: {str(e)}")
            return {"error": "Failed to retrieve comments."}

    @http_get('/{uuid:comment_id}', response=CommentDetailSchema)
    def get_comment_by_id(self, comment_id: uuid.UUID):
        """
        Retrieve details of a specific comment by its ID.

        Args:
            comment_id: The UUID of the comment to retrieve.

        Returns:
            CommentDetailSchema: The details of the requested comment.
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            logger.info(f"Comment retrieved: {comment.id}")
            return CommentDetailSchema.from_orm(comment)
        except Comment.DoesNotExist:
            logger.warning(f"Comment with ID {comment_id} not found.")
            return {"error": "Comment not found."}
        except Exception as e:
            logger.error(f"Error retrieving comment {comment_id}: {str(e)}")
            return {"error": "Failed to retrieve comment."}
