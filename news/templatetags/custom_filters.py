from django import template



register = template.Library()

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

bad_words = ["редиска", "Редиски", "петух гамбургской", "Новохудоноссор"]

@register.filter()  # фильтр для цензуры
def censor(value):
   for word in bad_words:
      if word.lower() in value.lower():
         value = value.replace(word[1:-2], '*' * (len(word)-1))
   return value


@register.filter(name='has_group') # фильтр проверяющий к какой группе относится юзер
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
