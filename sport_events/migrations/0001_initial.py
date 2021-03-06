# Generated by Django 3.1.2 on 2020-11-03 20:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('fee', models.IntegerField(default=0)),
                ('venue', models.CharField(max_length=50)),
                ('date_time', models.DateTimeField()),
                ('reg_close_date', models.DateField()),
                ('eligible_user_type', models.CharField(choices=[('STUDENT', 'Student'), ('TEACHER', 'Teacher')], max_length=10)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('CLOSED', 'Closed'), ('COMPLETED', 'Completed')], max_length=10)),
                ('curr_round', models.IntegerField(default=1)),
                ('participants', models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL)),
                ('sport', models.ForeignKey(on_delete=models.SET('Deleted Sport'), related_name='events', to='sport_events.sport')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
