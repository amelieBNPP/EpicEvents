# Generated by Django 3.2.12 on 2022-05-02 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('epicevents', '0005_alter_client_client_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
