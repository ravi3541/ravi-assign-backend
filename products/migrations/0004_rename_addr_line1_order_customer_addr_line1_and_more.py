# Generated by Django 4.0.6 on 2022-08-05 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_order_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='addr_line1',
            new_name='customer_addr_line1',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='addr_line2',
            new_name='customer_addr_line2',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='city',
            new_name='customer_city',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='country',
            new_name='customer_country',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='name',
            new_name='customer_name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='postal_code',
            new_name='customer_postal_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_state',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='tagline',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
