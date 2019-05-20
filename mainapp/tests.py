from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from mainapp.models import Card, CardCategory


class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        # response = self.client.get('/card/7/')
        # self.assertEqual(response.status_code, 200)

        response = self.client.get('/category/0/1/')
        self.assertEqual(response.status_code, 200)

        for category in CardCategory.objects.all():
            response = self.client.get(f'/category/{category.pk}/1/')
            self.assertEqual(response.status_code, 200)

        for card in Card.objects.all():
            response = self.client.get(f'/card/{card.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
