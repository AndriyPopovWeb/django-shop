# Generated by Django 4.0.3 on 2022-07-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_imageikio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageikio',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]