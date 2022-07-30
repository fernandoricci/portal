# Generated by Django 3.2 on 2022-05-25 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='estado_respuesta',
            field=models.CharField(blank=True, choices=[('Contestada', 'Contestada'), ('Sin contestar', 'Sin contestar'), ('En proceso', 'En proceso')], default='Sin contestar', max_length=15, null=True),
        ),
    ]