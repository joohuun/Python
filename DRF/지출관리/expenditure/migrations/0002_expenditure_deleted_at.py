# Generated by Django 4.1 on 2022-09-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenditure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True, verbose_name='삭제일'),
        ),
    ]
