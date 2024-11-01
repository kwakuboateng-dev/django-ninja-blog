from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

from base.api import PostController, CommentController


from ninja import Redoc

# Ninja Blog API Definition
api = NinjaExtraAPI(
    title="Django Ninja Blog API",
    version="1.0.0",
    description="""
        A RESTful API built with Django Ninja. 
        
        It offers comprehensive CRUD operations for managing blog posts and comments, 
        enhanced with JWT-based authentication, pagination, detailed logging, and rate limiting to ensure performance and security. 
        
        Designed for simplicity and extensibility, 
        the project includes custom management commands and automation scripts to streamline development and testing processes. 
        
        Whether you're building a personal blog platform or a content management system, 
        this API provides a robust foundation to support your needs.

        This project was assigned by Quame Jnr, a 🐐 in my books!
    """,
    throttle=[
        AnonRateThrottle('10/s'),
        AuthRateThrottle('100/s'),
    ],

    auth=JWTAuth(),

    # Uncomment to code below to change documentation to Redoc
    # docs=Redoc()
)

api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(PostController)
api.register_controllers(CommentController)
