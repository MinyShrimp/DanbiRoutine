# Generated by Django 4.0.3 on 2022-04-13 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=100)),
                ('pwd', models.BinaryField()),
                ('salt', models.BinaryField()),
                ('is_login', models.SmallIntegerField(default=0)),
                ('is_deleted', models.SmallIntegerField(default=0)),
                ('created_at', models.DateTimeField()),
                ('login_at', models.DateTimeField()),
                ('logout_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('routine_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('is_alarm', models.SmallIntegerField()),
                ('is_deleted', models.SmallIntegerField()),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'routine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoutineDay',
            fields=[
                ('day', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'routine_day',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoutineResult',
            fields=[
                ('routine_result_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.SmallIntegerField()),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'routine_result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
            ],
        ),
    ]
