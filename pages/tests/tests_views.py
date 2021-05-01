# pages.tests.tests_views.py

from django.test import TestCase
from django.urls import reverse, resolve


class HomepageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)
    
    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Bienvenue sur')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Salut ! Je ne devrais pas être sur la page.')

    # def test_homepage_url_resolves_homepageview(self):
    #     view = resolve('/')
    #     self.assertEqual(
    #         view.func.__name__,
    #         HomePageView.as_view().__name__
    #     )
