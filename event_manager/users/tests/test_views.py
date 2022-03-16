from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegisterTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')


class UserLoginTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(
            username='testuser1', password='Aa123123')

        test_user1.save()

        test_banned_user1 = User.objects.create_user(
            username='testuser2', password='Aa123123', is_active=False)

        test_banned_user1.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(
            response, '/login/?next=/profile/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(
            username='testuser1', password='Aa123123')
        response = self.client.get(reverse('profile'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_banned_user_login(self):
        self.client.login(
            username='testuser2', password='Aa123123')
        response = self.client.get(reverse('profile'))

        # Check that we got a response "failed" and moved to login
        self.assertEqual(response.status_code, 302)


class UserLogoutTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')
