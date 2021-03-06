# Generated by Django 4.0.4 on 2022-04-26 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=100)),
                ('list_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=13)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('additional1', models.CharField(max_length=30)),
                ('additional2', models.CharField(max_length=30)),
                ('list_name', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='smsApp.contactlist')),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_scheduled', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('statusCode', models.IntegerField(blank=True)),
                ('list_name', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='smsApp.contactlist')),
            ],
        ),
    ]
