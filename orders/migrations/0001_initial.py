# Generated by Django 3.2.2 on 2021-05-26 10:35

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '__first__'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyingInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=4, max_digits=15)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('product_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productoption')),
            ],
            options={
                'db_table': 'buying_informations',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='SellingInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=4, max_digits=15)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('product_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productoption')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'selling_informations',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('buying_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.buyinginformation')),
                ('selling_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.sellinginformation')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.AddField(
            model_name='buyinginformation',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.status'),
        ),
        migrations.AddField(
            model_name='buyinginformation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
