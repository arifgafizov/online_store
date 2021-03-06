# Generated by Django 3.1.7 on 2021-06-19 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210614_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preuser',
            options={'verbose_name': 'предварительный пользователь', 'verbose_name_plural': 'предварительные пользователи'},
        ),
        migrations.RemoveField(
            model_name='preuser',
            name='password',
        ),
        migrations.AddField(
            model_name='preuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None, verbose_name='дата создания'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='preuser',
            name='email',
            field=models.EmailField(max_length=150, verbose_name='ел. адрес'),
        ),
        migrations.AlterField(
            model_name='preuser',
            name='username',
            field=models.CharField(max_length=150, verbose_name='логин'),
        ),
    ]
