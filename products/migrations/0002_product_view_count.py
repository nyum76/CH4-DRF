# Generated by Django 4.2.8 on 2024-12-27 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='조회수'),
        ),
    ]
