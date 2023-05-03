from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'command help'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Comform exterminatus of all posts in a category {options["category"]}? yes/no:  _')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Canceled!'))
            return
        try:
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.category_name}')) # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {"category"}'))
