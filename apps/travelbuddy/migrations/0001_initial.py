# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 17:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.CharField(max_length=45)),
                ('destination', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('plan', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('pw_hash', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('b_day', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelbuddy.Users'),
        ),
    ]
