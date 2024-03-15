# Generated by Django 5.0.3 on 2024-03-15 12:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Post', '0001_initial'),
        ('User', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tashxis',
            name='bemor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.bemor'),
        ),
        migrations.AddField(
            model_name='tashxis',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
