# Generated by Django 3.1.6 on 2021-02-04 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0020_auto_20210204_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='date_ends',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='poll',
            name='date_starts',
            field=models.DateField(),
        ),
    ]
