# Generated by Django 5.0.3 on 2024-03-17 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0005_alter_tashxis_bemor_alter_tashxis_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tashxis',
            name='user',
        ),
    ]