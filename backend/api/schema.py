import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

# Import relay for the Node interface
from graphene import relay

# Import models
from .models import Author, Post, Comment

# Import filter classes
from .filters import AuthorFilter, PostFilter, CommentFilter


# Define GraphQL type for Author model
class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        interfaces = (relay.Node,)
        filterset_class = AuthorFilter


# Define GraphQL type for Post model
class PostType(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node,)
        filterset_class = PostFilter


# Define GraphQL type for Comment model
class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        filterset_class = CommentFilter


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
        author = Author(name=name, email=email, bio=bio)
        author.save()  # Save the author instance to the database
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
        author = Author.objects.get(pk=id)  # Fetch the author by ID
        if name:
            author.name = name
        if email:
            author.email = email
        if bio:
            author.bio = bio
        author.save()  # Save the updated author instance
        return UpdateAuthor(author=author)


# Mutation to delete an existing author
class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    # Mutation method to delete an author instance
    def mutate(self, info, id):
        author = Author.objects.get(pk=id)  # Fetch the author by ID
        author.delete()  # Delete the author instance
        return DeleteAuthor(ok=True)


# Mutation to create a new post
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.Int(required=True)

    post = graphene.Field(PostType)

    # Mutation method to create a new post instance
    def mutate(self, info, title, content, author_id):
        author = Author.objects.get(pk=author_id)  # Fetch the author by ID
        post = Post(title=title, content=content, author=author)
        post.save()  # Save the post instance to the database
        return CreatePost(post=post)


# Mutation to update an existing post
class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    # Mutation method to update an existing post instance
    def mutate(self, info, id, title=None, content=None):
        post = Post.objects.get(pk=id)  # Fetch the post by ID
        if title:
            post.title = title
        if content:
            post.content = content
        post.save()  # Save the updated post instance
        return UpdatePost(post=post)


# Mutation to delete an existing post
class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    # Mutation method to delete a post instance
    def mutate(self, info, id):
        post = Post.objects.get(pk=id)  # Fetch the post by ID
        post.delete()  # Delete the post instance
        return DeletePost(ok=True)


# Mutation to create a new comment
class CreateComment(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    comment = graphene.Field(CommentType)

    # Mutation method to create a new comment instance
    def mutate(self, info, content, post_id):
        post = Post.objects.get(pk=post_id)  # Fetch the post by ID
        comment = Comment(content=content, post=post)
        comment.save()  # Save the comment instance to the database
        return CreateComment(comment=comment)


# Mutation to update an existing comment
class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        content = graphene.String()

    comment = graphene.Field(CommentType)

    # Mutation method to update an existing comment instance
    def mutate(self, info, id, content=None):
        comment = Comment.objects.get(pk=id)  # Fetch the comment by ID
        if content:
            comment.content = content
        comment.save()  # Save the updated comment instance
        return UpdateComment(comment=comment)


# Mutation to delete an existing comment
class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    # Mutation method to delete a comment instance
    def mutate(self, info, id):
        comment = Comment.objects.get(pk=id)  # Fetch the comment by ID
        comment.delete()  # Delete the comment instance
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


# Combine all queries and mutations into a single schema
schema = graphene.Schema(query=Query, mutation=Mutation)
