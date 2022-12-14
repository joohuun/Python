# Generated by Django 4.1 on 2022-09-11 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('0', '의'), ('1', '식'), ('2', '주')], max_length=50, verbose_name='카테고리')),
            ],
            options={
                'db_table': '카테고리',
            },
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dec', models.TextField(verbose_name='설명')),
                ('amount', models.IntegerField(verbose_name='금액')),
                ('date', models.DateField(verbose_name='날짜')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화 여부')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='expenditure.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': '지출',
            },
        ),
        migrations.CreateModel(
            name='ExpenditureDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(verbose_name='세부 내용')),
                ('expenditure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='expenditure.expenditure', verbose_name='원글')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': '세부내용',
            },
        ),
    ]
