# Generated by Django 5.0.7 on 2024-11-23 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvu_destino', models.IntegerField(default=0)),
                ('monto', models.FloatField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]