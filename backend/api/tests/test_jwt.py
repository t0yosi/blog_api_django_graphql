from django.test import TestCase
from graphene_django.utils import GraphQLTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth.models import User
from ..models import Author, Post, Comment


class PostMutationTest(GraphQLTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = get_token(self.user)
        self.author = Author.objects.create(name="John Doe", email="john.doe@example.com")

    def test_create_post_authenticated(self):
        query = """
            mutation CreatePost($title: String!, $content: String!, $author_id: String!) {
              createPost(title: $title, content: $content, authorId: $author_id) {
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
            "author_id": str(self.author.id),  # Pass author ID as a string
        }
        response = self.client.post(
            "/graphql/",
            {"query": query, "variables": variables},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
            content_type="application/json",
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["createPost"]["post"]["title"], "New Post"
        )
