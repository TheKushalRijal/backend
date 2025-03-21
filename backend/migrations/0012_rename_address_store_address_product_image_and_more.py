# Generated by Django 5.1.4 on 2025-03-12 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_remove_store_api_key_remove_store_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='Address',
            new_name='address',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='parkings',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='store',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='store',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
