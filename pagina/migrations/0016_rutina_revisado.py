# Generated by Django 4.1.1 on 2022-12-21 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0015_alter_comentario_rutina_alter_feedback_rutina'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutina',
            name='revisado',
            field=models.BooleanField(default=False),
        ),
    ]
