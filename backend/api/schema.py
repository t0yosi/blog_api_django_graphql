import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

# Import JWT Decorators
from graphql_jwt.decorators import login_required

# Import relay for the Node interface
from graphene import relay

# Import models
from .models import Author, Post, Comment

# Import filter classes
from .filters import AuthorFilter, PostFilter, CommentFilter

import logging

logger = logging.getLogger(__name__)


# Define GraphQL type for Author model
class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        interfaces = (relay.Node,)
        filterset_class = AuthorFilter
        fields = "__all__"


# Define GraphQL type for Post model
class PostType(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node,)
        filterset_class = PostFilter
        fields = "__all__"


# Define GraphQL type for Comment model
class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        filterset_class = CommentFilter
        fields = "__all__"


#######################     FETCH DATA      ################################
class Query(graphene.ObjectType):
    # Define a query to fetch all authors
    all_authors = DjangoFilterConnectionField(AuthorType)
    # Define a query to fetch all posts
    all_posts = DjangoFilterConnectionField(PostType)
    # Define a query to fetch all comments
    all_comments = DjangoFilterConnectionField(CommentType)

    # Define a query to fetch a single post by ID
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))
    # Define a query to fetch a single author by ID
    author_by_id = graphene.Field(AuthorType, id=graphene.Int(required=True))
    # Define a query to fetch comments related to a specific post
    comments_by_post = DjangoFilterConnectionField(
        CommentType, post_id=graphene.Int(required=True)
    )

    # Resolver for fetching all authors
    def resolve_all_authors(root, info, **kwargs):
        return Author.objects.all()

    # Resolver for fetching all posts
    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    # Resolver for fetching all comments
    def resolve_all_comments(root, info, **kwargs):
        return Comment.objects.all()

    # Resolver for fetching a post by ID
    def resolve_post_by_id(root, info, id, **kwargs):
        return Post.objects.get(pk=id)

    # Resolver for fetching an author by ID
    def resolve_author_by_id(root, info, id, **kwargs):
        return Author.objects.get(pk=id)

    # Resolver for fetching comments by post ID
    def resolve_comments_by_post(root, info, post_id, **kwargs):
        return Comment.objects.filter(post_id=post_id)


########################     MODIFY DATA      ###############################
# Mutation to create a new author
class CreateAuthor(graphene.Mutation):
    # Define input arguments for the mutation
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        bio = graphene.String()

    # Define the output type
    author = graphene.Field(AuthorType)

    # Mutation method to create a new author instance
    def mutate(self, info, name, email, bio=None):
        logger.debug(f"Creating author with ID: {id}")
        author = Author(name=name, email=email, bio=bio)
        author.save()  # Save the author instance to the database
        logger.debug(f"Created author with ID: {author.id}")
        return CreateAuthor(author=author)


# Mutation to update an existing author
class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        email = graphene.String()
        bio = graphene.String()

    author = graphene.Field(AuthorType)

    # Mutation method to update an existing author instance
    def mutate(self, info, id, name=None, email=None, bio=None):
        logger.debug(f"Updating author with ID: {id}")
        author = Author.objects.get(pk=id)  # Fetch the author by ID
        if name:
            author.name = name
        if email:
            author.email = email
        if bio:
            author.bio = bio
        author.save()  # Save the updated author instance
        logger.debug(f"Updated author with ID: {author.id}")
        return UpdateAuthor(author=author)


# Mutation to delete an existing author
class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    # Mutation method to delete an author instance
    def mutate(self, info, id):
        logger.debug(f"Deleting author with ID: {id}")
        author = Author.objects.get(pk=id)  # Fetch the author by ID
        author.delete()  # Delete the author instance
        logger.debug(f"Deleted author with ID: {author.id}")
        return DeleteAuthor(ok=True)


# Mutation to create a new post
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.String(required=True)

    post = graphene.Field(PostType)

    # Mutation method to create a new post instance
    @login_required
    def mutate(self, info, title, content, author_id):
        user = info.context.user
        if not user.is_authenticated:
            logger.debug(f"403- Not Authenticated to create posts")
            raise Exception("Authentication credentials were not provided")

        # Ensure `author` is valid
        try:
            author = user.author_profile
        except Author.DoesNotExist:
            logger.debug(f"404- Author with ID {user.username} does not exist")
            raise Exception("Author does not exist")

        logger.debug(f"Creating post with title: {title} for author_id: {author.name}")
        # author = Author.objects.get(user=user)
        post = Post(title=title, content=content, author=author)
        post.save()  # Save the post instance to the database
        logger.debug(f"Created post with ID: {post.id}")
        return CreatePost(post=post)


# Mutation to update an existing post
class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    # Mutation method to update an existing post instance
    @login_required
    def mutate(self, info, id, title=None, content=None):
        user = info.context.user
        logger.debug(f"Updating post with ID: {id}")
        if not user.is_authenticated:
            logger.debug(f"403- Not Authenticated to update posts")
            raise Exception("Authentication credentials were not provided")
        logger.debug(f"Updating post with ID: {id}")
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            logger.debug(f"404- Post with ID {id} does not exist")
            raise Exception("Post does not exist")
        if post.author.user != user:
            logger.debug(f"403- Not permitted to update this post")
            raise Exception("You do not have permission to edit this post")
        if title:
            post.title = title
        if content:
            post.content = content
        post.save()  # Save the updated post instance
        logger.debug(f"Updated post with ID: {post.id}")
        return UpdatePost(post=post)


# Mutation to delete an existing post
class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    # Mutation method to delete a post instance
    @login_required
    def mutate(self, info, id):
        user = info.context.user
        logger.debug(f"Deleting post with ID: {id}")

         # Fetch the post by ID
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            logger.debug(f"404- Post with ID {id} does not exist")
            raise Exception("Post does not exist")

        if post.author.user != user:
            logger.debug(f"403- User {user.username} does not have permission to delete this post")
            raise Exception("You do not have permission to delete this post")
            
        post.delete()  # Delete the post instance
        logger.debug(f"CDeleted post with ID: {post.id}")
        return DeletePost(ok=True)


# Mutation to create a new comment
class CreateComment(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    comment = graphene.Field(CommentType)

    # Mutation method to create a new comment instance
    def mutate(self, info, content, post_id):
        logger.debug(f"Creating comment with content: {content} and post_id: {post_id}")
        post = Post.objects.get(pk=post_id)  # Fetch the post by ID
        comment = Comment(content=content, post=post)
        comment.save()  # Save the comment instance to the database
        logger.debug(f"Created comment with ID: {comment.id}")
        return CreateComment(comment=comment)


# Mutation to update an existing comment
class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        content = graphene.String()

    comment = graphene.Field(CommentType)

    # Mutation method to update an existing comment instance
    def mutate(self, info, id, content=None):
        logger.debug(f"Updating comment with ID: {id}")
        comment = Comment.objects.get(pk=id)  # Fetch the comment by ID
        if content:
            comment.content = content
        comment.save()  # Save the updated comment instance
        logger.debug(f"Updated comment with ID: {comment.id}")
        return UpdateComment(comment=comment)


# Mutation to delete an existing comment
class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    # Mutation method to delete a comment instance
    def mutate(self, info, id):
        logger.debug(f"Deleting comment with ID: {id}")
        comment = Comment.objects.get(pk=id)  # Fetch the comment by ID
        comment.delete()  # Delete the comment instance
        logger.debug(f"Deleted comment with ID: {comment.id}")
        return DeleteComment(ok=True)


#########################################################################
class Mutation(graphene.ObjectType):
    # Link each mutation to its corresponding class
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


# Combine all queries and mutations into a single schema
schema = graphene.Schema(query=Query, mutation=Mutation)
