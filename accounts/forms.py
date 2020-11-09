from django import forms

from listings.models import Category


class CategoryForm(forms.Form):
    Categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                to_field_name='title',
                                                label='Категорія (можна вибрати декілька)')
