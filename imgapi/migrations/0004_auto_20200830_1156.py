# Generated by Django 3.1 on 2020-08-30 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imgapi', '0003_auto_20200830_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='User',
            new_name='user',
        ),
    ]
