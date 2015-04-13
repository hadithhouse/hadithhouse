# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hadith',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HadithTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('brief_desc', models.CharField(max_length=128)),
                ('birth_year', models.SmallIntegerField(null=True, blank=True)),
                ('birth_month', models.SmallIntegerField(null=True, blank=True)),
                ('birth_day', models.SmallIntegerField(null=True, blank=True)),
                ('death_year', models.SmallIntegerField(null=True, blank=True)),
                ('death_month', models.SmallIntegerField(null=True, blank=True)),
                ('death_day', models.SmallIntegerField(null=True, blank=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hadith',
            name='person',
            field=models.ForeignKey(to='hadiths.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hadith',
            name='tags',
            field=models.ManyToManyField(to='hadiths.HadithTag'),
            preserve_default=True,
        ),
    ]