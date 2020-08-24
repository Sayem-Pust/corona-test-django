# Generated by Django 3.1 on 2020-08-22 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_form', '0002_auto_20200822_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='symptom',
        ),
        migrations.AddField(
            model_name='profile',
            name='symptom',
            field=models.ManyToManyField(blank=True, null=True, to='test_form.SymptomChoice'),
        ),
    ]