# Generated by Django 3.1.6 on 2021-02-03 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_answer_poll'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='question',
            name='poll',
        ),
    ]
