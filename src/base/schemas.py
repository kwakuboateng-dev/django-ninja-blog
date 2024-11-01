from ninja import Schema
from typing import Optional
from uuid import UUID
from ninja import ModelSchema, Schema
from .models import Post, Comment


class ErrorSchema(Schema):
    """
    Schema for error responses.

    - Contains a `detail` field to describe the error.
    """
    detail: str


class SuccessSchema(Schema):
    """
    Schema for success responses.

    - Contains a `message` field to describe the successful action.
    """
    message: str

# Schema for creating a new blog post


class PostCreateSchema(Schema):
    """
    Schema for creating a new blog post.

    Attributes:
        title: The title of the blog post.
        content: The content of the blog post.
    """
    title: str
    content: str


# Schema for updating an existing blog post
class PostUpdateSchema(Schema):
    """
    Schema for updating an existing blog post.

    All fields are optional, and only the provided fields will be updated.

    Attributes:
        title: The new title of the blog post (optional).
        content: The new content of the blog post (optional).
    """
    title: Optional[str] = None
    content: Optional[str] = None


class PostDetailSchema(Schema):
    """
    Schema for retrieving detailed information about a blog post.

    Attributes:
        id: The unique identifier of the blog post (UUID).
        title: The title of the blog post.
        content: The content of the blog post.
        author: The username of the author who created the post.
        created_at: The timestamp when the post was created, formatted as a string.
        updated_at: The timestamp when the post was last updated, formatted as a string.
    """
    id: UUID
    title: str
    content: str
    author: str
    created_at: str  # Convert to string
    updated_at: str  # Convert to string

    @classmethod
    def from_orm(cls, post):
        return cls(
            id=post.id,
            title=post.title,
            content=post.content,
            author=post.author.username,  # Convert the User object to a string
            created_at=post.created_at.isoformat(),  # Format datetime as string
            updated_at=post.updated_at.isoformat()  # Format datetime as string
        )


# Schema for creating a new comment
class CommentCreateSchema(Schema):
    """
    Schema for creating a new comment on a blog post.

    Attributes:
        post: The UUID of the blog post to which the comment belongs.
        text: The content of the comment.
    """
    post: UUID
    text: str


# Schema for updating an existing comment
class CommentUpdateSchema(Schema):
    """
    Schema for updating an existing comment.

    Only the text field is provided for updates.

    Attributes:
        text: The new content of the comment (optional).
    """
    text: Optional[str] = None


# Schema for retrieving detailed information about a comment
class CommentDetailSchema(Schema):
    """
    Schema for retrieving detailed information about a comment.

    Attributes:
        id: The unique identifier of the comment (UUID).
        post: The UUID of the blog post to which the comment belongs.
        author: The username of the author who created the comment.
        text: The content of the comment.
        created_at: The timestamp when the comment was created, formatted as a string.
    """
    id: UUID
    post: UUID
    author: str  # Display the author's username
    text: str
    created_at: str  # Convert to string

    @classmethod
    def from_orm(cls, comment):
        return cls(
            id=comment.id,
            post=comment.post.id,  # Use the UUID of the related post
            author=comment.author.username,  # Get the author's username
            text=comment.text,
            created_at=comment.created_at.isoformat()  # Format datetime as string
        )
