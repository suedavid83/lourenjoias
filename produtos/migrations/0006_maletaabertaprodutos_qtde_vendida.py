# Generated by Django 3.0.5 on 2021-12-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0005_view_maleta_aberta'),
    ]

    operations = [
        migrations.AddField(
            model_name='maletaabertaprodutos',
            name='qtde_vendida',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
