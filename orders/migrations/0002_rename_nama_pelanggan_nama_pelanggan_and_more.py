# Generated by Django 4.2.7 on 2024-12-01 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pelanggan',
            old_name='nama',
            new_name='nama_pelanggan',
        ),
        migrations.AddField(
            model_name='pelanggan',
            name='pesanan',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pemesanan',
            name='burger',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='menu.burger'),
            preserve_default=False,
        ),
    ]