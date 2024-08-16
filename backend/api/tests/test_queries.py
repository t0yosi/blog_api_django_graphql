from django.test import TestCase
from graphene_django.utils import GraphQLTestCase
from ..models import Author, Post, Comment
from ..schema import schema


class PostQueryTest(GraphQLTestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe", email="john.doe@example.com"
        )
        self.post = Post.objects.create(
            title="Sample Post", content="Sample content", author=self.author
        )
        self.comment = Comment.objects.create(content="Sample Comment", post=self.post)

    # Test for querying all posts
    def test_query_all_posts(self):
        query = """
            query {
              allPosts {
                edges {
                  node {
                    id
                    title
                    content
                  }
                }
              }
            }
            """
        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["allPosts"]["edges"][0]["node"]["title"],
            "Sample Post",
        )
        self.assertEqual(
            response.json()["data"]["allPosts"]["edges"][0]["node"]["content"],
            "Sample content",
        )

    # Test for querying a post by ID
    def test_query_post_by_id(self):
        query = (
            """
            query {
              postById(id: %s) {
                title
                content
              }
            }
            """
            % self.post.id
        )
        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(response.json()["data"]["postById"]["title"], "Sample Post")
        self.assertEqual(
            response.json()["data"]["postById"]["content"], "Sample content"
        )

    # Test for querying all authors
    def test_query_all_authors(self):
        query = """
            query {
              allAuthors {
                edges {
                  node {
                    id
                    name
                    email
                  }
                }
              }
            }
            """
        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.json()["data"]["allAuthors"]["edges"][0]["node"]["name"],
            "John Doe",
        )
        self.assertEqual(
            response.json()["data"]["allAuthors"]["edges"][0]["node"]["email"],
            "john.doe@example.com",
        )

    # Test for querying an author by ID
    def test_query_author_by_id(self):
        query = (
            """
            query {
              authorById(id: %s) {
                name
                email
              }
            }
            """
            % self.author.id
        )
        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(response.json()["data"]["authorById"]["name"], "John Doe")
        self.assertEqual(
            response.json()["data"]["authorById"]["email"], "john.doe@example.com"
        )

    # Test for querying comments by post ID
    def test_query_comments_by_post(self):
        query = (
            """
            query {
              commentsByPost(postId: %s) {
                edges {
                  node {
                    content
                  }
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
            response.json()["data"]["commentsByPost"]["edges"][0]["node"]["content"],
            "Sample Comment",
        )
