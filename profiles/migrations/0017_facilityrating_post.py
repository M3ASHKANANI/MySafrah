# Generated by Django 2.0.4 on 2018-05-09 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_facilityrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityrating',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='profiles.Post'),
            preserve_default=False,
        ),
    ]
