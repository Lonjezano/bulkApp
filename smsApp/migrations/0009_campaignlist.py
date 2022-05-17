# Generated by Django 4.0.4 on 2022-05-02 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smsApp', '0008_campaign_cost_campaign_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smsApp.campaign')),
            ],
        ),
    ]
