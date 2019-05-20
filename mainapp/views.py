
from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache

from mainapp.models import CardCategory, Card

# def get_menu():
#     return CardCategory.objects.filter(is_active=True).select_related()

def get_menu():
    if settings.LOW_CACHE:
        print('low cache menu')
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = CardCategory.objects.filter(is_active=True).select_related()
            cache.set(key, links_menu)
        return links_menu
    else:
        return CardCategory.objects.filter(is_active=True).select_related()

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(CardCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(CardCategory, pk=pk)


def get_cards():
    if settings.LOW_CACHE:
        key = 'card'
        card = cache.get(key)
        if card is None:
            card = Card.objects.filter(is_active=True,category__is_active=True).select_related()
            cache.set(key, card)
        return card
    else:
        return Card.objects.filter(is_active=True,category__is_active=True).select_related()


def get_card(pk):
    if settings.LOW_CACHE:
        key = f'card_{pk}'
        card = cache.get(key)
        if card is None:
            card = get_object_or_404(Card, pk=pk)
            cache.set(key, card)
        return card
    else:
        return get_object_or_404(Card, pk=pk)

def index(request):
    context = {
        'page_title': 'главная',
        'links_menu': get_menu(),
    }
    return render(request, 'mainapp/index.html', context)


def contacts(request):
    context = {
        'page_title' : 'контакты',
        'links_menu': get_menu(),
    }

    if request.is_ajax():
        
        result = render_to_string('mainapp/contacts.html', context)

        return JsonResponse({
                'content2': result,
            })
   
    else:
        return render(request, 'mainapp/contacts.html', context)

# @cache_page(3600)
# @never_cache
def category(request, pk, page=1):
      
    if int(pk) == 0:
        category = {
            'pk': 0,
            'name': 'все',
        }
        # card = Card.objects.filter(is_active=True, category__is_active=True).order_by('price')
        card = get_cards()
    else:
        category = get_category(pk)
        # category = get_object_or_404(CardCategory, pk=pk)
        card = category.card_set.filter(is_active=True).order_by('price')
    
    paginator = Paginator(card, 3)
    try:
        card = paginator.page(page)
    except PageNotAnInteger:
        card = paginator.page(1)
    except EmptyPage:
        card = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'товары',
        'links_menu': get_menu(),
        'category': category,
        'cards': card,
    }

    if request.is_ajax():
        result = render_to_string('mainapp/includes/inc__cards_list_content.html', 
                                  context=context,
                                  request=request)
        
        return JsonResponse({'result': result})

    else:

        return render(request, 'mainapp/catalog.html', context)

# @never_cache
def card(request, pk):
    context = {
        'page_title': 'продукт',
        # 'links_menu': CardCategory.objects.all(),
        'links_menu': get_menu(),
        # 'object': get_object_or_404(Card, pk=pk),
        'object': get_card(pk),
    }
    return render(request, 'mainapp/card.html', context)

