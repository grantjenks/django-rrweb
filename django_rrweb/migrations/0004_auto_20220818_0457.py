# Generated by Django 3.2.15 on 2022-08-18 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('django_rrweb', '0003_auto_20220818_0457'),
    ]

    operations = [
        migrations.RunSQL(
            """
            INSERT INTO django_rrweb_page
            SELECT id, create_time, key, id AS session_id
            FROM django_rrweb_session
            """
        ),
        migrations.RunSQL(
            """
            UPDATE django_rrweb_event
            SET page_id = (
                SELECT id
                FROM django_rrweb_page
                WHERE django_rrweb_page.session_id = django_rrweb_event.session_id
            )
            """
        ),
        migrations.RemoveField(
            model_name='event',
            name='session',
        ),
        migrations.AlterField(
            model_name='event',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='django_rrweb.page'),
        ),
    ]