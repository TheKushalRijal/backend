# Generated by Django 5.1.4 on 2025-03-12 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inStock',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
