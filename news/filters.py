import django_filters
from django import forms
from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter
from django.forms.widgets import DateInput, SelectMultiple

from .models import Category, Post


class PostFilter(FilterSet):
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