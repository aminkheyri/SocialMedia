# Generated by Django 3.1.7 on 2021-03-28 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(default='0', max_length=700),
            preserve_default=False,
        ),
    ]
