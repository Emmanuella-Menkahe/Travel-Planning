# Generated by Django 5.1 on 2024-10-14 20:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_travelplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_places', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_card_number', models.CharField(max_length=50)),
                ('reserved_at', models.DateTimeField(auto_now_add=True)),
                ('travel_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.travelplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
