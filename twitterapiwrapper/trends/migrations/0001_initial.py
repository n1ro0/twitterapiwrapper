# Generated by Django 2.0.1 on 2018-01-19 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('tweet_volume', models.IntegerField()),
                ('url', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('created_at', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('hashtags', models.ManyToManyField(related_name='tweets', to='trends.Hashtag')),
                ('trend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trends.Trend')),
            ],
        ),
    ]
