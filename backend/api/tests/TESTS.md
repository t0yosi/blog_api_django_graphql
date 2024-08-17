# Comprehensive Tests Documentation

## GraphQL Mutation Tests

### `test_create_post`
Tests the creation of a post.

### `test_update_post`
Tests the updating of an existing post.

### `test_delete_post`
Tests the deletion of a post.

### `test_create_author`
Tests the creation of an author.

### `test_update_author`
Tests the updating of an existing author.

### `test_delete_author`
Tests the deletion of an author.

### `test_create_comment`
Tests the creation of a comment.

### `test_update_comment`
Tests the updating of an existing comment.

### `test_delete_comment`
Tests the deletion of a comment.

## GraphQL Query Tests

### `test_query_all_posts`
Tests querying all posts.

### `test_query_post_by_id`
Tests querying a post by its ID.

### `test_query_all_authors`
Tests querying all authors.

### `test_query_author_by_id`
Tests querying an author by their ID.

### `test_query_comments_by_post`
Tests querying comments related to a specific post.

## Django Model Tests

### `test_author_creation`
Tests the creation of an author in the Django model.

### `test_post_creation`
Tests the creation of a post in the Django model.

### `test_comment_creation`
Tests the creation of a comment in the Django model.

## Test Cases

### SignUp Mutation Test
Tests the `signUp` mutation to ensure a user can sign up correctly and receive a token.

### Comment Signal Test
Tests that the `updated_at` field on a post is updated when a comment is created or updated.

### Post Mutation Test
Tests the creation of a post with authenticated access using a GraphQL mutation.

## TO RUN TESTS

1. Setup the project as instructed in the root directory README file.
2. Run `pytest` in the terminal.
3. Wait for results.
