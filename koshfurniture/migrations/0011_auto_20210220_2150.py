# Generated by Django 3.1.5 on 2021-02-20 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('koshfurniture', '0010_auto_20210220_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
    ]
