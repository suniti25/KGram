# Generated by Django 3.2.5 on 2021-07-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_alter_postmodel_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
