# Generated by Django 2.2.13 on 2020-07-30 12:54

from django.db import migrations, models
import partial_date.partial_date


class Migration(migrations.Migration):

    dependencies = [
        ('installations', '0007_auto_20200715_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliography',
            name='year',
            field=partial_date.partial_date.PartialDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='materialevidence',
            name='date',
            field=partial_date.partial_date.PartialDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sourcetype',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
