# Generated by Django 3.0.6 on 2020-07-10 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='visible',
            field=models.BooleanField(default='False'),
        ),
    ]
