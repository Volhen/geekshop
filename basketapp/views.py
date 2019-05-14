from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from mainapp.models import Card
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def index(request):
    
    return render(request, 'basketapp/index.html')

# @login_required
# def add(request, pk):
#     if 'login' in request.META.get('HTTP_REFERER'):
#         return HttpResponseRedirect(reverse('main:card',
#                                             kwargs={
#                                                 'pk': pk,
#                                             }))

#     card = get_object_or_404(Card, pk=pk)
#     basket = Basket.objects.filter(user=request.user, card=card).first()

#     if not basket:
#         basket = Basket(user=request.user, card=card)

#     basket.quantity += 1
#     # basket.card.quantity -= 1
#     # basket.card.save()
#     basket.save()

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    get_object_or_404(Basket, pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update(request, pk, quantity):
    if request.is_ajax():
        basket= get_object_or_404(Basket, pk=int(pk))
        quantity = int(quantity)
        if quantity > 0:
            # basket.card.quantity -= quantity - basket.quantity
            # basket.card.save()
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        context = {
            'basket': request.user.basket.all().order_by('card__category'),
        }
        result = render_to_string('basketapp/includes/inc__basket_list.html', context)

        return JsonResponse({
            'result': result
        })

@login_required
def add(request, pk):
    if request.is_ajax():

        card = get_object_or_404(Card, pk=pk)
        basket = Basket.objects.filter(user=request.user, card=card).first()

        if not basket:
            basket = Basket(user=request.user, card=card)

        basket.quantity += 1
        basket.save()
        
        return JsonResponse({
            'basket_total_quantity': basket.total_quantity,
            'basket_total_cost': basket.total_cost
        })