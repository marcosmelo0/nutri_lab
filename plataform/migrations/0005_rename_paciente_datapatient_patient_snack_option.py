# Generated by Django 5.0 on 2023-12-28 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataform', '0004_datapatient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datapatient',
            old_name='paciente',
            new_name='patient',
        ),
        migrations.CreateModel(
            name='Snack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('horario', models.TimeField()),
                ('carboidratos', models.IntegerField()),
                ('proteinas', models.IntegerField()),
                ('gorduras', models.IntegerField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataform.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='option')),
                ('description', models.TextField()),
                ('snack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataform.snack')),
            ],
        ),
    ]
