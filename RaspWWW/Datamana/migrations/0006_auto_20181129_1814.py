# Generated by Django 2.1.2 on 2018-11-29 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Datamana', '0005_auto_20181129_1812'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datapoint',
            options={'ordering': ['datetime']},
        ),
    ]
