# Generated by Django 5.1.1 on 2024-10-01 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_Code', models.CharField(max_length=6)),
                ('door_No', models.PositiveIntegerField()),
                ('road_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=4)),
                ('address', models.CharField(max_length=255)),
                ('followers', models.PositiveBigIntegerField()),
                ('description', models.TextField(max_length=255)),
                ('logo', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('metatag', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField()),
                ('stock', models.PositiveIntegerField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.products')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.address')),
            ],
            options={
                'ordering': ['-email'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('product_rating', models.FloatField(max_length=255)),
                ('date', models.DateField(auto_now=True)),
                ('location', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.PositiveIntegerField()),
                ('time_of_order', models.DateTimeField()),
                ('status', models.CharField(choices=[('C', 'Completed'), ('D', 'Denied'), ('P', 'Pending')], default='P', max_length=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.user')),
            ],
        ),
    ]