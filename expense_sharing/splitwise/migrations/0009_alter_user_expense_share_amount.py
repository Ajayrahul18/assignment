# Generated by Django 4.2.7 on 2023-11-16 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splitwise', '0008_user_expense_share_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expense_share_amount',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
