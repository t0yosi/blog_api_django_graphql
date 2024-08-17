from django.test import TestCase
from graphene.test import Client
from api.schema import schema

class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_sign_up(self):
        mutation = """
            mutation {
                signUp(username: "newuser", password: "password123", email: "newuser@example.com", name: "New User") {
                    user {
                        id
                        username
                        email
                    }
                    token
                }
            }
        """
        response = self.client.execute(mutation)
        content = response

        # Check if the mutation was successful
        self.assertIn('data', content)
        self.assertIn('signUp', content['data'])
        self.assertIsNotNone(content['data']['signUp']['token'])
        self.assertEqual(content['data']['signUp']['user']['username'], 'newuser')
        self.assertEqual(content['data']['signUp']['user']['email'], 'newuser@example.com')

        # Optional: Check if there are any errors
        if 'errors' in content:
            self.fail(f"GraphQL errors occurred: {content['errors']}")
