# Generated by Django 5.2.1 on 2025-06-01 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourShop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='posted_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 6, 1, 10, 0, 22, 921094, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
