# Generated by Django 5.0.7 on 2024-08-01 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_hashtag_post_hashtags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text_content',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_content',
            field=models.TextField(max_length=1000),
        ),
    ]