# Generated by Django 4.1 on 2022-09-12 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
