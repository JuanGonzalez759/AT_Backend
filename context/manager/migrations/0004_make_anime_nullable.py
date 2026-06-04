from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_add_manga_to_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='anime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_watchlists', to='backoffice.anime'),
        ),
    ]
