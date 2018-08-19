# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-09 07:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名字')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('url', models.URLField(verbose_name='网址')),
                ('content', models.TextField(verbose_name='评论')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
    ]
