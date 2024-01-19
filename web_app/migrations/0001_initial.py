# Generated by Django 5.0 on 2023-12-20 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Visitor",
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
                ("user", models.CharField(max_length=30)),
                ("password", models.CharField(max_length=20)),
                ("name", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=30)),
                ("vertified", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "visitor",
            },
        ),
    ]
