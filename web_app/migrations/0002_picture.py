# Generated by Django 5.0 on 2023-12-27 06:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Picture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("filename", models.CharField(max_length=50)),
                ("picture", models.ImageField(upload_to="static/pictures")),
            ],
            options={
                "db_table": "picture",
            },
        ),
    ]
