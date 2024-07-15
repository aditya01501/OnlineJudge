# Generated by Django 5.0.6 on 2024-07-13 12:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_leaderboard_score'),
        ('question', '0003_delete_submission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('verdict', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=20)),
                ('contest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.contests')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]