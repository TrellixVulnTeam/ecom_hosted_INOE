# Generated by Django 3.0.7 on 2020-09-07 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200907_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(default='NEW', max_length=200),
            preserve_default=False,
        ),
    ]
