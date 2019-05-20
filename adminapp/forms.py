from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from authapp.models import GeekUser
from django import forms

from mainapp.models import CardCategory, Card


class ShopUserCreationAdminForm(UserCreationForm):
    class Meta:
        model = GeekUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data


class ShopUserUpdateAdminForm(UserChangeForm):
    class Meta:
        model = GeekUser
        # fields = '__all__'
        fields = ('username', 'first_name', 'last_name', 'email',
                  'age', 'avatar', 'password', 'is_superuser', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data


class ProductCategoryEditForm(forms.ModelForm):

    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = CardCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # field.help_text = ''



class ShopUserRecoverAdminForm(UserChangeForm):
    class Meta:
        model = GeekUser
        # fields = '__all__'
        fields = ('is_superuser', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            