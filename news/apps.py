from django.apps import AppConfig
import redis


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'


red = redis.Redis(
    host='redis-17703.c293.eu-central-1-1.ec2.cloud.redislabs.com',
    port=17703,
    password='LUmQ0FOlqLbSGkRVL9DfHfXhMiyqdvf2'
)
