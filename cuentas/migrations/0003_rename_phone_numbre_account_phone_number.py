# Generated by Django 3.2 on 2022-05-21 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0002_alter_account_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='phone_numbre',
            new_name='phone_number',
        ),
    ]
