# Generated by Django 3.2.12 on 2022-06-29 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(max_length=100)),
                ('product_code', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'BaseProducts',
                'db_table': 'base_products',
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('creator_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Creator',
                'db_table': 'creator',
            },
        ),
        migrations.CreateModel(
            name='LargeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'LargeCategory',
                'db_table': 'largecategory',
            },
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('season', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Seasons',
                'db_table': 'seasons',
            },
        ),
        migrations.CreateModel(
            name='SmallCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('largecategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.largecategory')),
            ],
            options={
                'verbose_name_plural': 'SmallCategory',
                'db_table': 'smallcategory',
            },
        ),
        migrations.CreateModel(
            name='SeasonsRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('baseproduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.baseproducts')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.seasons')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('detail_name', models.CharField(max_length=100)),
                ('detail_code', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('tags', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('memo', models.TextField(blank=True, default=None, max_length=1000, null=True)),
                ('base_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.baseproducts')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('picture', models.FileField(blank=True, default=None, null=True, upload_to='picture/%Y/%m/%d')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.products')),
            ],
            options={
                'verbose_name_plural': 'Pictures',
                'db_table': 'pictures',
            },
        ),
        migrations.CreateModel(
            name='Materials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('material_name', models.CharField(blank=True, max_length=200, null=True)),
                ('volume', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.products')),
            ],
            options={
                'verbose_name_plural': 'Materials',
                'db_table': 'materials',
            },
        ),
        migrations.AddField(
            model_name='baseproducts',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.creator'),
        ),
        migrations.AddField(
            model_name='baseproducts',
            name='seasons',
            field=models.ManyToManyField(through='product.SeasonsRelation', to='product.Seasons'),
        ),
        migrations.AddField(
            model_name='baseproducts',
            name='small_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.smallcategory'),
        ),
    ]
