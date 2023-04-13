from django_filters import FilterSet, DateFilter
from django.forms.widgets import DateInput
from .models import Post


class PostFilter(FilterSet):
    # post_type_choice = ChoiceFilter(choices=[('ar', 'Article'), ('nw', 'News')])


    date_published = DateFilter(field_name='t_creation', lookup_expr='gte',
                                widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        # В Meta классе мы должны указать Django модел в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = {
            'title': ['icontains'],
            # 't_creation': ['gt'],
            # 'post_types': ['post_type_choice']
        }


