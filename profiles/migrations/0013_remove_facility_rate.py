# Generated by Django 2.0.4 on 2018-05-08 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20180508_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='rate',
        ),
    ]
