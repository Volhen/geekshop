from django.db import models

class CardCategory(models.Model):
    name = models.CharField(verbose_name='название', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', db_index=True, default=True)
    
    def __str__(self):
        return self.name

class Card(models.Model):
    category = models.ForeignKey(CardCategory, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='cards_images', blank=True)
    name = models.CharField(verbose_name='название карты', max_length=128)
    title = models.TextField(verbose_name='описание карты товара', blank=True)
    price = models.DecimalField(verbose_name='цена товара', max_digits=8, decimal_places=2, default=0)
    quantity = models.SmallIntegerField(verbose_name='количество товара', default=0)
    is_active = models.BooleanField(verbose_name='активен', db_index=True, default=True)
    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @staticmethod
    def get_items():
        return Card.objects.filter(category__is_active=True, is_active=True).order_by('category', 'name')