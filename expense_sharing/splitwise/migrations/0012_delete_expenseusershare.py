# Generated by Django 4.2.7 on 2023-11-16 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('splitwise', '0011_expense_date_individualexpense'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExpenseUserShare',
        ),
    ]