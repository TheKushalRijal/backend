# Generated by Django 5.1.4 on 2025-03-11 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_delete_token_item_store_store_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='finaltokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tokens', models.CharField(max_length=100)),
            ],
        ),
    ]
