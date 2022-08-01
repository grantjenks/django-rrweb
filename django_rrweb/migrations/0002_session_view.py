from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rrweb', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE VIEW django_rrweb_session AS
                SELECT
                    session_key,
                    MIN(create_time) AS create_time,
                    MIN(user_id) AS user_id,
                    MIN(timestamp) AS timestamp,
                    MAX(timestamp) - MIN(timestamp) AS duration,
                    COUNT(data) AS event_count,
                    SUM(LENGTH(data)) AS event_size
                FROM django_rrweb_event
                GROUP BY session_key
            """,
            reverse_sql='DROP VIEW django_rrweb_session',
            hints={'target_db': 'default', 'model_name': 'Session'}
        ),
    ]
