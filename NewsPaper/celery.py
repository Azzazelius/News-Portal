import os
from celery import Celery


# Окружение DJANGO_SETTINGS_MODULE, настройки проекта NewsPaper
# через DJANGO_SETTINGS_MODULE django понимает что настройки celery надо брать из этого файла
# и использовать для проекта NewsPaper.
# Поэтому в когда в view.py запускается метод notify.delay() celery знает, что надо брать настройки из celery.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper') # экземпляр приложения Celery
app.config_from_object('django.conf:settings', namespace='CELERY')  # использовать настройки из settings.py
# в документации к celery рекомендуется всегда использовать именование namespace='CELERY'
app.autodiscover_tasks() # Загрузить задачи из всех модулей с именем "tasks.py"

if __name__ == '__main__':
    # Запуск Celery как асинхронного процесса
    app.start()



