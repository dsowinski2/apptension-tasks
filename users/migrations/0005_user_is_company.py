# Generated by Django 3.2.5 on 2021-09-06 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210906_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_company',
            field=models.BooleanField(default=False),
        ),
    ]
