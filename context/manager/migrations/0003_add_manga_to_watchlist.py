# Generated manually to add manga FK to Watchlist
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_watchlist'),
        ('backoffice', '0009_manga'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='manga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_watchlists_manga', to='backoffice.manga'),
        ),
        migrations.AlterModelOptions(
            name='watchlist',
            options={'verbose_name': 'Watchlist Item', 'verbose_name_plural': 'Watchlist Items', 'ordering': ['-added_at']},
        ),
    ]
