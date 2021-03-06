# Generated by Django 3.1.7 on 2021-03-27 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0004_auto_20210327_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('additional_info', models.JSONField(blank=True, default=dict, verbose_name='Дополнительные настройки')),
                ('delivery_at', models.DateTimeField(verbose_name='дата доставки')),
                ('address', models.CharField(max_length=200, verbose_name='адрес доставки')),
                ('phone', models.CharField(max_length=50, verbose_name='номер телефона')),
                ('status', models.CharField(choices=[('created', 'создан'), ('delivered', 'доставлен'), ('processed', 'обработан'), ('cancelled', 'отменено')], max_length=100, verbose_name='статус заказа')),
                ('cart', models.ForeignKey(help_text='корзина заказа', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='carts.cart')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]
