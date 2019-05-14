from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from django.forms.models import inlineformset_factory
from basketapp.models import Basket
from ordersapp.forms import OrderItemForm, OrderForm
from ordersapp.models import Order, OrderItem
from mainapp.models import Card


class OrderList(ListView):
    model = Order

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.basket.all()
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['card'] = basket_items[num].card
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].card.price
            else:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            self.request.user.basket.all().delete()
        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    # form_class = OrderForm
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
 
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.card.price
            data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            self.request.user.basket.all().delete()
            # self.request.user.basket.all().first().delete()
        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
   model = Order
   success_url = reverse_lazy('order:orders_list')


class OrderRead(DetailView):
   model = Order

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['title'] = 'заказ/просмотр'
       return context


def order_forming_complete(request, pk):
   order = get_object_or_404(Order, pk=pk)
   order.status = Order.SENT_TO_PROCEED
   order.save()

   return HttpResponseRedirect(reverse('order:orders_list'))

def get_product_price(request, pk):
       if request.is_ajax():
            card = Card.objects.filter(pk=int(pk)).first()
            if card:
                return JsonResponse({'price': card.price})
            else:
                return JsonResponse({'price': 0})

@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def card_quantity_update_save(sender, update_fields, instance, **kwargs):
    # print(f'pre_save -> {sender}')
    # if update_fields is 'quantity' or 'card':
    if instance.pk:
        instance.card.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.card.quantity -= instance.quantity
    instance.card.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def card_quantity_update_delete(sender, instance, **kwargs):
    print(f'pre_delete -> {sender}')
    instance.card.quantity += instance.quantity
    instance.card.save()