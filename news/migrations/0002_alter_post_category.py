# Generated by Django 4.2 on 2023-04-19 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(blank=True, through='news.PostCategory', to='news.category', verbose_name='Категории'),
        ),
    ]