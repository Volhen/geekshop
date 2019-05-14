from django.db import models
from django.conf import settings
from mainapp.models import Card

# class BasketQuerySet(models.QuerySet):  
#     def delete(self, *args, **kwargs):
#         print('model manager delete')
#         for obj in self:
#             obj.card.quantity += obj.quantity
#             obj.card.save()
#         super().delete(*args, **kwargs)

class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.card.price * self.quantity

    @property
    def total_quantity(self):
        "return total quantity for user"
        return sum(list(map(lambda x: x.quantity, self.user.basket.all())))

    @property
    def total_cost(self):
        "return total cost for user"
        return sum(list(map(lambda x: x.product_cost, self.user.basket.all())))
    
    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.card.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.card.quantity -= self.quantity
    #     self.card.save()
    #     super().save(*args, **kwargs)

    # def delete(self):
    #     print('model delete')
    #     self.card.quantity += self.quantity
    #     self.card.save()
    #     super().delete()
