# Generated by Django 2.1.4 on 2018-12-30 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_auto_20181230_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestdata',
            name='session_key',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='requestdata',
            name='time',
            field=models.IntegerField(default=1546197105.8761),
        ),
    ]