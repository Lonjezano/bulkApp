# Generated by Django 4.0.4 on 2022-04-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsApp', '0004_alter_campaign_statuscode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='message',
            field=models.TextField(help_text='Write your Message here', max_length=140),
        ),
    ]
