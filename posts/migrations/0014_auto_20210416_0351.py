# Generated by Django 3.1.7 on 2021-04-15 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_vote_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pvote', to='posts.post'),
        ),
    ]
