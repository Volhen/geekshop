# Generated by Django 2.1.7 on 2019-04-16 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to='cards_images')),
                ('name', models.CharField(max_length=128, verbose_name='название карты')),
                ('title', models.TextField(blank=True, verbose_name='описание карты товара')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена товара')),
                ('quantity', models.SmallIntegerField(default=0, verbose_name='количество товара')),
                ('is_active', models.BooleanField(default=True, verbose_name='активен')),
            ],
        ),
        migrations.CreateModel(
            name='CardCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='активна')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.CardCategory'),
        ),
    ]