# Generated by Django 5.1.7 on 2025-04-14 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_alter_comments_data_coments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='data_coments',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 14, 15, 45, 53, 681166, tzinfo=datetime.timezone.utc), verbose_name='Дата коментарии'),
        ),
    ]
