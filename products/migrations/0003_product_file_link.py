# Generated by Django 3.1.7 on 2021-07-03 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210309_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='file_link',
            field=models.CharField(default='', max_length=256, verbose_name='файл'),
            preserve_default=False,
        ),
    ]
