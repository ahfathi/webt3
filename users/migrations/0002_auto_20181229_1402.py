# Generated by Django 2.1.4 on 2018-12-29 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatars/info.png', upload_to='avatars'),
        ),
    ]
