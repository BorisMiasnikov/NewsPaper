# Generated by Django 5.0.1 on 2024-02-17 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='choice_field',
            field=models.CharField(choices=[('N', 'Новость'), ('A', 'Статья')], default='A', max_length=1),
        ),
    ]
