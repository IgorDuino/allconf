# Generated by Django 4.0.4 on 2022-05-22 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_lecture_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='file',
            field=models.FileField(
                upload_to='files/',
                verbose_name='Презентация'),
        ),
    ]
