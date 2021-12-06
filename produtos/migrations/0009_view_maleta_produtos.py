# Generated by Django 3.0.5 on 2021-12-04 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0008_auto_20211204_0535'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIEW_MALETA_PRODUTOS',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('vendedor', models.CharField(max_length=20)),
                ('nome_vendedor', models.CharField(max_length=20)),
                ('id_maletaaberta', models.IntegerField()),
                ('nome_maleta', models.CharField(max_length=30)),
                ('cod_produto', models.CharField(max_length=20)),
                ('des_produto', models.CharField(max_length=100)),
                ('quantidade', models.IntegerField()),
                ('qtde_vendida', models.IntegerField()),
            ],
            options={
                'db_table': 'VIEW_MALETA_PRODUTOS',
                'managed': False,
            },
        ),
    ]
