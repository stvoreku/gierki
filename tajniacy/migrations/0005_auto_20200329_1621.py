# Generated by Django 3.0 on 2020-03-29 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tajniacy', '0004_auto_20200328_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
