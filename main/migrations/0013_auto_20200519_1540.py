# Generated by Django 3.0.6 on 2020-05-19 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200517_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='union',
            name='occupationReason',
            field=models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='Причина занятости'),
        ),
    ]
