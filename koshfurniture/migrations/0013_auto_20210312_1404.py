# Generated by Django 3.1.5 on 2021-03-12 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('koshfurniture', '0012_auto_20210312_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='koshfurniture.customer'),
        ),
    ]
