# Generated by Django 4.1.1 on 2022-12-08 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedexdjango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='legendary',
            field=models.CharField(blank=True, default=None, max_length=150, null=True),
        ),
    ]
