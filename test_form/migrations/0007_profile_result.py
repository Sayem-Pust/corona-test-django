# Generated by Django 3.1 on 2020-08-23 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_form', '0006_auto_20200822_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='result',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]