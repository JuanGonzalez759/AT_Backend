from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0009_manga'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('title', models.CharField(blank=True, max_length=255)),
                ('language', models.CharField(default='es', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='backoffice.manga')),
            ],
            options={'ordering': ['number'], 'unique_together': {('manga', 'number')}},
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField()),
                ('image', models.FileField(upload_to='mangas/%Y/%m/%d/')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='backoffice.chapter')),
            ],
            options={'ordering': ['page_number']},
        ),
    ]
