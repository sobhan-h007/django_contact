# Generated by Django 4.1 on 2022-08-11 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactlist', '0004_alter_contact_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]