# Generated by Django 3.2.2 on 2024-03-24 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='point_value',
            field=models.IntegerField(default=0),
        ),
    ]