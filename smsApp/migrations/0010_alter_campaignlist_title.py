# Generated by Django 4.0.4 on 2022-05-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsApp', '0009_campaignlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignlist',
            name='title',
            field=models.CharField(default='defaul', max_length=255),
        ),
    ]