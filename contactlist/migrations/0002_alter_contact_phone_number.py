# Generated by Django 3.2.4 on 2022-08-02 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.IntegerField(max_length=11),
        ),
    ]
