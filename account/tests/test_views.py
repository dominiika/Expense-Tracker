from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):

        self.signup_url = reverse('signup')
        self.client = Client()

    def test_signup_GET(self):

        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('account/signup.html')
