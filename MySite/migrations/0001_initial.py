# Generated by Django 4.2.5 on 2023-10-01 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('matric_no', models.CharField(max_length=12)),
                ('dob', models.DateField()),
                ('program', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=50)),
            ],
        ),
    ]