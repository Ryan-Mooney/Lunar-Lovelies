# Generated by Django 2.1.2 on 2018-11-22 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('picture_url', models.URLField(max_length=500)),
                ('image1', models.ImageField(default='images/no-image-found.png', null=True, upload_to='images')),
                ('image2', models.ImageField(default='images/no-image-found.png', null=True, upload_to='images')),
                ('image3', models.ImageField(default='images/no-image-found.png', null=True, upload_to='images')),
                ('image4', models.ImageField(default='images/no-image-found.png', null=True, upload_to='images')),
                ('price', models.FloatField(default=0.0)),
                ('category', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=5000)),
                ('filters', models.CharField(default='None', max_length=5000)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('paypal_button', models.CharField(max_length=5000)),
                ('out_of_stock', models.BooleanField(default=False)),
            ],
        ),
    ]