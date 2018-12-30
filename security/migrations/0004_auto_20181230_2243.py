# Generated by Django 2.1.4 on 2018-12-30 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0003_auto_20181230_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestdata',
            name='time',
            field=models.IntegerField(default=1546197195.870189),
        ),
        migrations.AlterField(
            model_name='requestdata',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
