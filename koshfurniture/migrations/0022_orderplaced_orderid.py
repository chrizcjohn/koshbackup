# Generated by Django 3.1.5 on 2021-03-13 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('koshfurniture', '0021_remove_orderplaced_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='orderId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='koshfurniture.order'),
        ),
    ]
