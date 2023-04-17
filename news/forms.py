from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author',
        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "content": "Текст не может быть менее 20 символов."
            })

        name = cleaned_data.get("title")
        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data