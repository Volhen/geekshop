def basket(request):
    # print(f'context processor basket works')
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.all().order_by('card__category').select_related()
    return {
        'basket': basket,
    }