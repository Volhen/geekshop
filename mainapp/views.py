
from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mainapp.models import CardCategory, Card

def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def get_menu():
    return CardCategory.objects.filter(is_active=True).select_related()


def contacts(request):
    context = {
        'page_title' : 'контакты',
    }

    if request.is_ajax():
        
        result = render_to_string('mainapp/contacts.html', context)

        return JsonResponse({
                'content2': result,
            })
   
    else:
        return render(request, 'mainapp/contacts.html', context)


def category(request, pk, page=1):
  
    if int(pk) == 0:
        category = {
            'pk': 0,
            'name': 'все',
        }
        card = Card.objects.filter(is_active=True, category__is_active=True).order_by('price')
    else:
        category = get_object_or_404(CardCategory, pk=pk)
        card = category.card_set.filter(is_active=True).order_by('price')
    
    paginator = Paginator(card, 3)
    try:
        card = paginator.page(page)
    except PageNotAnInteger:
        card = paginator.page(1)
    except EmptyPage:
        card = paginator.page(paginator.num_pages)

    context = {
        'title': 'товары',
        'links_menu': get_menu(),
        'category': category,
        'cards': card,
    }

    if request.is_ajax():
        
        return JsonResponse({
            'content2': context,
        })

    else:

        return render(request, 'mainapp/catalog.html', context)


def card(request, pk):
    context = {
        'title': 'продукт',
        'links_menu': CardCategory.objects.all(),
        'object': get_object_or_404(Card, pk=pk),
    }
    return render(request, 'mainapp/card.html', context)

