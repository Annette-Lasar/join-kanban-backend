# Generated by Django 5.1.5 on 2025-02-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0009_alter_category_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color_brightness',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
