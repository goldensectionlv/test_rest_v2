# Generated by Django 3.1.6 on 2021-02-03 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0017_auto_20210203_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='poll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poll_user_answers', to='poll.poll'),
        ),
    ]
