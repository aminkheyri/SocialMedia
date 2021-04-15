# Generated by Django 3.1.7 on 2021-04-13 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0006_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='to_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='following', to='auth.user'),
            preserve_default=False,
        ),
    ]