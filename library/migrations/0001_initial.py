import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Category', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=100, unique=True)),
        ]),
        migrations.CreateModel(name='Book', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('title', models.CharField(max_length=200)), ('author', models.CharField(max_length=150)),
            ('isbn', models.CharField(max_length=20, unique=True)),
            ('total_copies', models.PositiveIntegerField(default=1)),
            ('available_copies', models.PositiveIntegerField(default=1)),
            ('description', models.TextField(blank=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='library.category')),
        ]),
        migrations.CreateModel(name='Member', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=150)), ('email', models.EmailField(max_length=254, unique=True)),
            ('phone', models.CharField(blank=True, max_length=20)),
            ('student_id', models.CharField(max_length=50, unique=True)),
            ('joined_at', models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name='Loan', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('issue_date', models.DateField(default=django.utils.timezone.localdate)),
            ('due_date', models.DateField()), ('return_date', models.DateField(blank=True, null=True)),
            ('status', models.CharField(choices=[('ISSUED', 'Issued'), ('RETURNED', 'Returned')], default='ISSUED', max_length=10)),
            ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loans', to='library.book')),
            ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loans', to='library.member')),
        ], options={'ordering': ['-issue_date', '-id']}),
    ]
