# Generated by Django 5.0.1 on 2024-03-04 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_checkoutadd_phone_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_delivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_received',
        ),
        migrations.RemoveField(
            model_name='order',
            name='razorpay_signature',
        ),
    ]
