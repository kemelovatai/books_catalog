# Generated by Django 4.1.3 on 2022-11-03 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookRating',
        ),
    ]