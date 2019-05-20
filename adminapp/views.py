from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

from adminapp.forms import ShopUserCreationAdminForm, ShopUserUpdateAdminForm, ProductCategoryEditForm, ShopUserRecoverAdminForm, CardEditForm
from authapp.models import GeekUser
from mainapp.models import CardCategory, Card


class UsersListView(ListView):
    model = GeekUser
    # template_name = 'adminapp/index.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    object_list = CardCategory.objects.all().order_by('-is_active', 'name')
    context = {
        'title': 'админка/категории',
        'object_list': object_list
    }
    return render(request, 'adminapp/cardcategory_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def cards(request, pk):
    category = get_object_or_404(CardCategory, pk=pk)
    object_list = category.card_set.all().order_by('name')
    context = {
        'title': 'админка/продукт',
        'category': category,
        'object_list': object_list,
    }
    return render(request, 'adminapp/card_list.html', context)

def shopuser_create(request):
    if request.method == 'POST':
        form = ShopUserCreationAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserCreationAdminForm()
    context = {
        'title': 'пользователи/создание',
        'form': form
    }
    return render(request, 'adminapp/shopuser_update.html', context)


def shopuser_update(request, pk):
    current_user = get_object_or_404(GeekUser, pk=pk)
    if request.method == 'POST':
        form = ShopUserUpdateAdminForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserUpdateAdminForm(instance=current_user)
    context = {
        'title': 'пользователи/редактирование',
        'form': form
    }
    return render(request, 'adminapp/shopuser_update.html', context)


def shopuser_delete(request, pk):
    object = get_object_or_404(GeekUser, pk=pk)
    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('myadmin:index'))
    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': object
    }
    return render(request, 'adminapp/shopuser_delete.html', context)

def shopuser_recover(request, pk):
    current_user = get_object_or_404(GeekUser, pk=pk)
    if request.method == 'POST':
        form = ShopUserRecoverAdminForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserRecoverAdminForm(instance=current_user)
    context = {
        'title': 'пользователи/востановить',
        'form': form
    }
    return render(request, 'adminapp/shopuser_update.html', context)


class ProductCategoryCreateView(CreateView):
    model = CardCategory
    success_url = reverse_lazy('myadmin:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm


def productcategory_update(request, pk):
    current_object = get_object_or_404(CardCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryEditForm(request.POST, request.FILES, instance=current_object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:categories'))
    else:
        form = ProductCategoryEditForm(instance=current_object)
    context = {
        'title': 'категории/редактирование',
        'form': form
    }
    return render(request, 'adminapp/productcategory_update.html', context)


class ProductCategoryUpdateView(UpdateView):
    model = CardCategory
    success_url = reverse_lazy('myadmin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context
    
    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.card_set.update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)



class ProductCategoryDeleteView(DeleteView):
    model = CardCategory
    success_url = reverse_lazy('myadmin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def card_create(request,pk):
    category = get_object_or_404(CardCategory, pk=pk)
    if request.method == 'POST':
        form = CardEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:cards',kwargs={'pk': pk}))
    else:
        form = CardEditForm(initial={'category': category})
    context = {
        'title': 'карты/создание',
        'form': form,
        'category': category
    }
    return render(request, 'adminapp/card_update.html', context)

class ProductDetailView(DetailView):
    model = Card


def card_update(request, pk):
    product_object = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = CardEditForm(request.POST, request.FILES, instance=product_object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:cards',
                                                kwargs={'pk': product_object.category.pk}))
    else:
        form = CardEditForm(instance=product_object)
    context = {
        'title': 'товары/редактирование',
        'form': form,
        'category': product_object.category
    }
    return render(request, 'adminapp/card_update.html', context)


def card_delete(request, pk):
    object = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('myadmin:cards',
                                            kwargs={'pk': object.category.pk}))
    context = {
        'title': 'товары/удаление',
        'object': object,
        'category': object.category
    }
    return render(request, 'adminapp/card_delete.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

@receiver(pre_save, sender=CardCategory)
def card_is_active_update_cardtcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.card_set.update(is_active=True)
        else:
            instance.card_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)