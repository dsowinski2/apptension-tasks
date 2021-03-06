# Generated by Django 3.2.5 on 2021-09-13 07:49

from django.db import migrations, models
from django.db.models import Q, Case, When, Value

def set_account_type(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.all().update(
        account_type=Case(
            When((Q(is_company=True) & Q(is_admin=True)) , then=Value('PREMIUM')),
                default=Value('FREE')
        )
    )

def delete_account_type(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.all().update(account_type=None)    

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210913_0737'),
    ]

    operations = [
        migrations.RunPython(set_account_type, reverse_code=delete_account_type)

    ]
