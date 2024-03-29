# Generated by Django 5.0.3 on 2024-03-17 04:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0003_rename_sick_tashxis_diagnoz_tashxis_tashxis'),
        ('User', '0002_remove_bemor_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='tashxis',
            name='bemor',
            field=models.ForeignKey(default='uchirilgan bemor', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tashxis_user', to='User.bemor'),
        ),
        migrations.AlterField(
            model_name='tashxis',
            name='user',
            field=models.ForeignKey(default='uchirilgan user', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tashxis_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
