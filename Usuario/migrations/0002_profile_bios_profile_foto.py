# Generated by Django 5.2 on 2025-04-17 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bios',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='foto',
            field=models.ImageField(default='uploads/foto_perfil/DefaultProfileImage.png', upload_to='uploads/fotos_perfil/'),
        ),
    ]
