# Generated by Django 4.0.6 on 2022-08-05 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_addr_line1_order_customer_addr_line1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_email',
            field=models.EmailField(max_length=255),
        ),
    ]
