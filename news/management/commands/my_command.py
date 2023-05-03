from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'command help'  # ���������� ��������� ��� ����� "python manage.py <���� �������> --help"
    missing_args_message = 'insufficient args'
    requires_migrations_checks = True  # ���������� �� � ���������. ���� true � �� ����� ����������� � ���, ��� �� ������� ��� �������� (���� ����� ����)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        # ����� ������ ������ ����� ���, ������� ����������� ��� ������ ����� �������
        self.stdout.write(str(options['argument']))
