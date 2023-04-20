import django_filters
from django import forms
from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter
from django.forms.widgets import DateInput, SelectMultiple

from .models import Category, Post


class PostFilter(FilterSet):
    # post_type_choice = ChoiceFilter(choices=[('ar', 'Article'), ('nw', 'News')])
    title = CharFilter(label='Заголовок содержит')
    date_published = DateFilter(field_name='t_creation', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}),
                                label='Дата публикации после:')

    class Meta:
        model = Post
        fields = [
            'title',
            'date_published',
            'category',
            'author',
        ]


# class CategoryFilter(FilterSet):
#     categories = django_filters.ModelMultipleChoiceFilter(
#         label='Категории',
#         queryset=Category.objects.all(),
#         field_name='categories',
#         widget=SelectMultiple(attrs={
#             'class': 'selectpicker',
#             'data-live-search': 'true',
#             # 'multiple': True,
#             'style': 'display: flex; align-items: center;',
#         }),
#     )
#
#     class Meta:
#         model = Post
#         fields = [
#             'categories',
#         ]


class CategoryFilter(FilterSet):
    categories = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        }),
        label="Категории",
    )

    class Meta:
        model = Post
        fields = ['categories']