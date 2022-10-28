# Generated by Django 4.1.2 on 2022-10-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traka', '0003_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['first_name', 'last_name', 'user__email', 'user__mobile', 'country', 'gender']},
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]