# Generated by Django 2.0.4 on 2018-05-03 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20180503_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traveltype',
            name='Friends',
        ),
        migrations.RemoveField(
            model_name='traveltype',
            name='backpack',
        ),
        migrations.RemoveField(
            model_name='traveltype',
            name='business',
        ),
        migrations.RemoveField(
            model_name='traveltype',
            name='couple',
        ),
        migrations.RemoveField(
            model_name='traveltype',
            name='family',
        ),
        migrations.RemoveField(
            model_name='traveltype',
            name='medical',
        ),
        migrations.RemoveField(
            model_name='traveltype',
            name='solo',
        ),
        migrations.AddField(
            model_name='traveltype',
            name='title',
            field=models.CharField(default='somesome', max_length=120),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='profile',
            name='travelpref',
        ),
        migrations.AddField(
            model_name='profile',
            name='travelpref',
            field=models.ManyToManyField(to='profiles.Traveltype'),
        ),
    ]
