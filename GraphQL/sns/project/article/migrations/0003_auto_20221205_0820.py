# Generated by Django 3.1.2 on 2022-12-05 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20221205_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article'),
        ),
    ]
