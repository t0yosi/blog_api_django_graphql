from django.test import TestCase
from graphene_django.utils import GraphQLTestCase
from ..models import Author, Post, Comment
from ..schema import schema
from django.contrib.auth.models import User
from graphql_jwt.shortcuts import get_token


class PostMutationTest(GraphQLTestCase):
    def setUp(self):
          self.user = User.objects.create_user(username="testuser", password="testpass")
          self.token = get_token(self.user)
          self.author = Author.objects.create(
              user=self.user,  # Link the user to the author
              name="John Doe",
              email="john.doe@example.com",
          )
          self.post = Post.objects.create(
              title="Post Title", content="Post content", author=self.author
          )
          self.comment = Comment.objects.create(content="Comment content", post=self.post)

    # Example test method with authentication
    def test_create_post(self):
        query = """
            mutation CreatePost($title: String!, $content: String!, $authorId: String!) {
              createPost(title: $title, content: $content, authorId: $authorId) {
                post {
                  title
                  content
                }
              }
            }
        """
        variables = {
            "title": "New Post",
            "content": "New content",
            "authorId": str(self.author.id),
        }
        response = self.client.post(
            "/graphql/",
            {"query": query, "variables": variables},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",  # Pass the JWT token
            content_type="application/json",
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["createPost"]["post"]["title"], "New Post"
        )
        self.assertEqual(
            response.json()["data"]["createPost"]["post"]["content"], "New content"
        )

    # Test for updating a post
    def test_update_post(self):
        query = """
            mutation UpdatePost($id: Int!, $title: String!, $content: String!) {
              updatePost(id: $id, title: $title, content: $content) {
                post {
                  title
                  content
                }
              }
            }
        """
        variables = {
            "id": self.post.id,
            "title": "Updated Title",
            "content": "Updated content",
        }

        response = self.client.post(
            "/graphql/",
            {"query": query, "variables": variables},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
            content_type="application/json",
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["updatePost"]["post"]["title"], "Updated Title"
        )
        self.assertEqual(
            response.json()["data"]["updatePost"]["post"]["content"], "Updated content"
        )

    # Test for deleting a post
    def test_delete_post(self):
        query = """
            mutation DeletePost($id: Int!) {
              deletePost(id: $id) {
                ok
              }
            }
        """
        variables = {"id": self.post.id}

        response = self.client.post(
            "/graphql/",
            {"query": query, "variables": variables},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",  # Include the JWT token
            content_type="application/json",
        )

        self.assertResponseNoErrors(response)
        self.assertTrue(response.json()["data"]["deletePost"]["ok"])
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    # Test for creating an author
    def test_create_author(self):
        query = """
            mutation {
              createAuthor(name: "Jane Doe", email: "jane.doe@example.com", bio: "Bio") {
                author {
                  name
                  email
                  bio
                }
              }
            }
            """

        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["createAuthor"]["author"]["name"], "Jane Doe"
        )
        self.assertEqual(
            response.json()["data"]["createAuthor"]["author"]["email"],
            "jane.doe@example.com",
        )
        self.assertEqual(
            response.json()["data"]["createAuthor"]["author"]["bio"], "Bio"
        )

    # Test for updating an author
    def test_update_author(self):
        query = (
            """
            mutation {
              updateAuthor(id: %s, name: "Updated Name", email: "updated.email@example.com") {
                author {
                  name
                  email
                }
              }
            }
            """
            % self.author.id
        )

        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["updateAuthor"]["author"]["name"], "Updated Name"
        )
        self.assertEqual(
            response.json()["data"]["updateAuthor"]["author"]["email"],
            "updated.email@example.com",
        )

    # Test for deleting an author
    def test_delete_author(self):
        query = (
            """
            mutation {
              deleteAuthor(id: %s) {
                ok
              }
            }
            """
            % self.author.id
        )

        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        self.assertResponseNoErrors(response)
        self.assertTrue(response.json()["data"]["deleteAuthor"]["ok"])
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())

    # Test for creating a comment
    def test_create_comment(self):
        query = (
            """
            mutation {
              createComment(content: "New Comment", postId: %s) {
                comment {
                  content
                }
              }
            }
            """
            % self.post.id
        )

        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["createComment"]["comment"]["content"],
            "New Comment",
        )

    # Test for updating a comment
    def test_update_comment(self):
        query = (
            """
            mutation {
              updateComment(id: %s, content: "Updated Comment") {
                comment {
                  content
                }
              }
            }
            """
            % self.comment.id
        )

        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["updateComment"]["comment"]["content"],
            "Updated Comment",
        )

    # Test for deleting a comment
    def test_delete_comment(self):
        query = (
            """
            mutation {
              deleteComment(id: %s) {
                ok
              }
            }
            """
            % self.comment.id
        )

        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        self.assertResponseNoErrors(response)
        self.assertTrue(response.json()["data"]["deleteComment"]["ok"])
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
