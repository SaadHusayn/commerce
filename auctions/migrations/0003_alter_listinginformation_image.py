# Generated by Django 5.0.2 on 2024-07-03 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listinginformation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listinginformation',
            name='image',
            field=models.ImageField(blank=True, upload_to='auctions/images/'),
        ),
    ]
