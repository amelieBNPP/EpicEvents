# Generated by Django 3.2.12 on 2022-04-07 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compagny_name', models.CharField(max_length=250)),
                ('last_contact', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField()),
                ('client_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('payment_due', models.DateField(auto_now_add=True)),
                ('client_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epicevents.client')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(max_length=250)),
                ('role', models.CharField(choices=[('manager', 'Manager'), ('sales', 'Sales'), ('support', 'Support')], max_length=25)),
                ('employee_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now_add=True)),
                ('event_date', models.DateField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, max_length=2048)),
                ('attendees', models.IntegerField()),
                ('closed', models.BooleanField()),
                ('contract_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epicevents.contract')),
                ('support_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epicevents.employee')),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epicevents.employee'),
        ),
        migrations.AddField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epicevents.employee'),
        ),
    ]
