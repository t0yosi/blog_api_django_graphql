from django.test import TestCase
from django.utils import timezone
from ..models import Author, Post, Comment
from django.db.models.signals import post_save
from ..schema import schema
from django.contrib.auth.models import User

class CommentSignalTestCase(TestCase):
    def setUp(self):
        # Create a user and author for the post
        self.user = User.objects.create_user(username='testuser', password='password')
        self.author = Author.objects.create(user=self.user, name="Test Author", email="testauthor@example.com")
        
        # Create a post instance for testing
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.author
        )

    def test_comment_creation_updates_post(self):
        # Capture the initial updated_at value
        initial_updated_at = self.post.updated_at
        
        # Create a comment related to the post
        Comment.objects.create(
            content="This is a test comment.",
            post=self.post,
        )
        
        # Refresh the post instance to get the updated values
        self.post.refresh_from_db()
        
        # Check if the updated_at field has been updated
        self.assertGreater(self.post.updated_at, initial_updated_at)
    
    def test_comment_update_updates_post(self):
        # Create a comment related to the post
        comment = Comment.objects.create(
            content="This is a test comment.",
            post=self.post,
        )
        
        # Capture the initial updated_at value
        initial_updated_at = self.post.updated_at
        
        # Update the comment
        comment.content = "Updated comment content."
        comment.save()
        
        # Refresh the post instance to get the updated values
        self.post.refresh_from_db()
        
        # Check if the updated_at field has been updated
        self.assertGreater(self.post.updated_at, initial_updated_at)
