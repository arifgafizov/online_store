# Generated by Django 3.1.7 on 2021-04-03 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210329_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=11, verbose_name='Стоимость заказа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'создан'), ('delivered', 'доставлен'), ('processed', 'обработан'), ('cancelled', 'отменено')], default='created', max_length=100, verbose_name='статус заказа'),
        ),
    ]