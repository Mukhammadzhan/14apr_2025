# Generated by Django 5.1.7 on 2025-04-08 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_posts_data_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='data_publication',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 8, 18, 21, 31, 332127, tzinfo=datetime.timezone.utc), verbose_name='Дата публикации'),
        ),
    ]
