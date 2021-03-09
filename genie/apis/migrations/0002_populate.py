from django.db import migrations
from django.utils import timezone

def populate_db(apps, schema_editor):
    Event = apps.get_model('apis', 'Event')

    for i in range(10):
        event = Event(
            name = "Event " + str(i),
            date = timezone.now()
        )
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]
