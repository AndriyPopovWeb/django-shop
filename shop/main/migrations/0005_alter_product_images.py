# Generated by Django 4.0.3 on 2022-04-09 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, to='main.image'),
        ),
    ]
