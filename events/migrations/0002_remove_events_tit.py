# Generated by Django 3.1.1 on 2020-09-20 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='tit',
        ),
    ]
