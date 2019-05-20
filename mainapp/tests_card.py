from django.test import TestCase
from mainapp.models import Card, CardCategory


class CardsTestCase(TestCase):
    def setUp(self):
        category = CardCategory.objects.create(name="стулья")
        self.card_1 = Card.objects.create(name="стул 1",
                                                category=category,
                                                price=1999.5,
                                                quantity=150)

        self.card_2 = Card.objects.create(name="стул 2",
                                                category=category,
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False)

        self.card_3 = Card.objects.create(name="стул 3",
                                                category=category,
                                                price=998.1,
                                                quantity=115)

    def test_card_get(self):
        card_1 = Card.objects.get(name="стул 1")
        card_2 = Card.objects.get(name="стул 2")
        self.assertEqual(card_1, self.card_1)
        self.assertEqual(card_2, self.card_2)

    def test_card_print(self):
        card_1 = Card.objects.get(name="стул 1")
        card_2 = Card.objects.get(name="стул 2")
        self.assertEqual(str(card_1), 'стул 1 (стулья)')
        self.assertEqual(str(card_2), 'стул 2 (стулья)')

    def test_card_get_items(self):
        card_1 = Card.objects.get(name="стул 1")
        card_3 = Card.objects.get(name="стул 3")
        cards = Card.get_items()

        self.assertEqual(list(cards), [card_1, card_3])
