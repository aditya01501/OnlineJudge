# Generated by Django 5.0.6 on 2024-07-13 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='code',
            field=models.TextField(null=True),
        ),
    ]