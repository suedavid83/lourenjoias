# Generated by Django 3.0.5 on 2021-11-26 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cliente', models.CharField(max_length=100)),
                ('endereco', models.CharField(blank=True, max_length=200, null=True)),
                ('bairro', models.CharField(max_length=30)),
                ('cidade', models.CharField(blank=True, max_length=30, null=True)),
                ('estado', models.CharField(blank=True, max_length=2, null=True)),
                ('cep', models.CharField(max_length=20)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=200)),
                ('whatsapp', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('nome_vendedor', models.CharField(max_length=100)),
                ('cpf_cnpj', models.CharField(max_length=50)),
                ('rg', models.CharField(max_length=20)),
                ('endereco', models.CharField(max_length=200)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=20)),
                ('telefone', models.CharField(max_length=20)),
                ('id_maleta', models.IntegerField()),
                ('ref1_empresa', models.CharField(max_length=50)),
                ('ref1_contato', models.CharField(max_length=30)),
                ('ref1_telefone', models.CharField(max_length=20)),
                ('ref2_empresa', models.CharField(max_length=50)),
                ('ref2_contato', models.CharField(max_length=30)),
                ('ref2_telefone', models.CharField(max_length=20)),
            ],
        ),
    ]