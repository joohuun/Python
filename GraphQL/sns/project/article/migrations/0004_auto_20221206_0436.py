# Generated by Django 3.1.2 on 2022-12-06 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20221205_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.article'),
        ),
    ]
