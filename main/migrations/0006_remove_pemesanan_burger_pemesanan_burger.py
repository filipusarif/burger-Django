# Generated by Django 4.2.7 on 2024-12-01 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_pemesanan_total_harga'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pemesanan',
            name='burger',
        ),
        migrations.AddField(
            model_name='pemesanan',
            name='burger',
            field=models.ManyToManyField(to='main.burger'),
        ),
    ]
