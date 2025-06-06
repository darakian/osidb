# Generated by Django 4.2.16 on 2024-12-10 14:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=255, unique=True)),
                ('type', models.CharField(choices=[('ALLOWLIST', 'Allowlist'), ('ALLOWLIST_SPECIAL_CASE', 'Allowlist Special Case'), ('BLOCKLIST', 'Blocklist'), ('BLOCKLIST_SPECIAL_CASE', 'Blocklist Special Case')], max_length=25)),
            ],
        ),
    ]
