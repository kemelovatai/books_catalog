# Generated by Django 4.1.3 on 2022-11-03 07:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_delete_bookrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='biography',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Биография'),
        ),
    ]
