# Generated by Django 5.0.2 on 2024-02-15 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Team",
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
                ("name", models.CharField(max_length=255)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Team",
                "verbose_name_plural": "Teams",
                "db_table": "team",
                "ordering": ("-created_date",),
            },
        ),
    ]
