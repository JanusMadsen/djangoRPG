# Generated by Django 4.2.16 on 2024-10-16 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPG', '0015_player_model_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player_model',
            name='name',
            field=models.CharField(default='Placeholder', max_length=100),
        ),
    ]
