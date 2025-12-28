from django.test import TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    """Test cases for the main app views"""

    def test_home_page_status_code(self):
        """Test that the home page returns a 200 status code"""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Test that the home page uses the correct template"""
        response = self.client.get(reverse('main:home'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_about_page_status_code(self):
        """Test that the about page returns a 200 status code"""
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """Test that the about page uses the correct template"""
        response = self.client.get(reverse('main:about'))
        self.assertTemplateUsed(response, 'main/about.html')

    def test_home_page_content(self):
        """Test that the home page contains expected content"""
        response = self.client.get(reverse('main:home'))
        self.assertContains(response, 'Welcome to ORT Django Web App!')

    def test_about_page_content(self):
        """Test that the about page contains expected content"""
        response = self.client.get(reverse('main:about'))
        self.assertContains(response, 'About ORT Django Web App')
