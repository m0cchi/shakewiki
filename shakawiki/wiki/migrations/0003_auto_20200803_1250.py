# Generated by Django 3.0.8 on 2020-08-03 12:50

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_article_by'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='article',
            managers=[
                ('public_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
