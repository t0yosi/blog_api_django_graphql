from django.test import TestCase
from ..models import Author, Post, Comment


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe", email="john.doe@example.com"
        )

    def test_author_creation(self):
        # Check that the Author was created with the correct attributes
        self.assertEqual(self.author.name, "John Doe")
        self.assertEqual(self.author.email, "john.doe@example.com")

    def test_author_str_method(self):
        # Optional: Check the string representation of the Author model (if applicable)
        self.assertEqual(str(self.author), "John Doe")


class PostModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe", email="john.doe@example.com"
        )
        self.post = Post.objects.create(
            title="Sample Post", content="Sample content", author=self.author
        )

    def test_post_creation(self):
        # Check that the Post was created with the correct attributes
        self.assertEqual(self.post.title, "Sample Post")
        self.assertEqual(self.post.content, "Sample content")
        self.assertEqual(self.post.author, self.author)

    def test_post_str_method(self):
        # Optional: Check the string representation of the Post model (if applicable)
        self.assertEqual(str(self.post), "Sample Post")


class CommentModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe", email="john.doe@example.com"
        )
        self.post = Post.objects.create(
            title="Sample Post", content="Sample content", author=self.author
        )
        self.comment = Comment.objects.create(content="Sample comment", post=self.post)

    def test_comment_creation(self):
        # Check that the Comment was created with the correct attributes
        self.assertEqual(self.comment.content, "Sample comment")
        self.assertEqual(self.comment.post, self.post)

    def test_comment_str_method(self):
        # Check the string representation of the Comment model
        self.assertEqual(
            str(self.comment), f"Comment on {self.post.title} by {self.comment.id}"
        )
