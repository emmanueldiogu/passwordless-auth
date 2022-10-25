# Generated by Django 4.1.2 on 2022-10-22 21:25

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=60)),
                ('language', models.CharField(max_length=60)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='M', max_length=1)),
                ('height', models.DecimalField(decimal_places=2, max_digits=6)),
                ('height_unit', models.CharField(choices=[('cm', 'centimeters'), ('ft', 'feets')], default='cm', max_length=2)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('weight_unit', models.CharField(choices=[('kg', 'kilogram'), ('lb', 'pounds')], default='kg', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
