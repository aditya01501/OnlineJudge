# Generated by Django 5.0.6 on 2024-07-13 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0007_remove_score_id_alter_score_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Score',
        ),
    ]
