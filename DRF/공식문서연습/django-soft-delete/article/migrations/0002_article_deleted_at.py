# Generated by Django 4.1 on 2022-09-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
