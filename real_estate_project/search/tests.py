from django.test import TestCase
from .models import House


# Create your tests here.

class AnimalTestCase(TestCase):
    @staticmethod
    def test_get_data():
        print(House.objects.all())
