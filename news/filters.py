from django import forms
from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter
from django_filters.rest_framework import filters
from django.forms.widgets import DateInput, SelectMultiple
from datetime import datetime, timedelta, time
from django.utils import timezone

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


class WeeklyPostFilter(FilterSet):
    date_published = filters.DateFilter(field_name='t_creation', method='filter_weekly_posts')

    def filter_weekly_posts(self, queryset, name, value):
        today = timezone.now().date()
        last_monday = today - timezone.timedelta(days=today.weekday(), weeks=1)
        last_monday = timezone.datetime.combine(last_monday, timezone.time.min)
        return queryset.filter(t_creation__gte=last_monday)

    class Meta:
        model = Post
        fields = ['date_published']