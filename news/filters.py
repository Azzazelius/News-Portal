import django_filters
from django import forms
from django_filters import FilterSet, DateFilter, CharFilter
from django.forms.widgets import DateInput
from .models import Category


class PostFilter(FilterSet):
    # post_type_choice = ChoiceFilter(choices=[('ar', 'Article'), ('nw', 'News')])
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок содержит')
    date_published = DateFilter(field_name='t_creation', lookup_expr='gte',
                                widget=DateInput(attrs={'type': 'date'}), label='Дата публикации после:')

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'selectpicker',
            'data-live-search': 'true',
            'multiple': True,
            'style': 'display: flex; align-items: center;',
        }))

    # автор

# категории
#     category =

#
# class Meta:
#     # В Meta классе мы должны указать Django модел в которой будем фильтровать записи.
#     model = Post
#     # В fields мы описываем по каким полям модели будет производиться фильтрация.
#     fields = {
#         'category'
#     }
#
#     widgets = {'category': SelectMultiple(attrs={'class': 'form-control'})}
#
#
