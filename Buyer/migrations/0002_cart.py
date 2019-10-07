# Generated by Django 2.1.8 on 2019-09-16 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField()),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_price', models.FloatField()),
                ('goods_count', models.IntegerField()),
                ('goods_picture', models.CharField(max_length=32)),
                ('goods_total_price', models.FloatField()),
                ('cart_user', models.IntegerField()),
            ],
        ),
    ]