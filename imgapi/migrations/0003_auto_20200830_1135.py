# Generated by Django 3.1 on 2020-08-30 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('imgapi', '0002_auto_20200830_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
    ]