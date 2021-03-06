# Generated by Django 3.2.12 on 2022-03-13 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagination.schoolinfo')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.AddIndex(
            model_name='schoolinfo',
            index=models.Index(fields=['name'], name='school_name'),
        ),
    ]
