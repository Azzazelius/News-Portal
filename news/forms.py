from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError

from .models import Post, Category






class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
            'author',
        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "description": "Текст не может быть менее 20 символов."  # заменить дескрипшен на contern?
            })

        name = cleaned_data.get("title")
        if name == description:
            raise ValidationError({
                "title": "Описание не должно быть идентично названию."  # почему проверки не срабатывают?
            })
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        if not valid:  # если форма не прошла стандартные проверки, ничего не делаем
            valid = False

        title = self.cleaned_data.get("title")  # дополнительные проверки формы
        if len(title) < 5:
            self.add_error("title", "Название должно содержать не менее 5 символов.")
            valid = False

        content = self.cleaned_data.get("content")
        if len(content) < 20:
            self.add_error("content", "Содержание должно содержать не менее 20 символов.")
            valid = False

        return valid


class SubscribeForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple,

    )
