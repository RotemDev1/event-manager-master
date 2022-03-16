from django.test import TestCase
from ..forms import UserRegisterForm

class userCreationFormTest(TestCase):

    def test_valid_data(self):
        data = {'username': 'testuser', 'email': 'test@company.com', 'password1': 'testing1234', 'password2': 'testing1234'}
        form = UserRegisterForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        data = {'username': 111, 'email': '', 'password1': 'testing1234', 'password2': 'testing1234'}
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_required_missing(self):
        data = {'username': 'testuser', 'password1': 'testing1234', 'password2': 'testing1234'}
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
                
    def test_weak_password(self):
        data = {'username': 'testuser', 'email': 'test@company.com', 'password1': '1234', 'password2': '1234'}
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_unmatched_passwords(self):
        data = {'username': 111,'email': '', 'password1': 'testing1234', 'password2': '1234testing'}
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
