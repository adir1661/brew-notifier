# Generated by Django 4.0.5 on 2022-07-03 13:24

from django.db import migrations, models
import django.db.models.deletion
import notifier.consts
import notifier.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('crawling_status', models.CharField(choices=[(0, 'NOT_CRAWLED'), (1, 'ERROR_REQUESTING_LINK'), (2, 'UPDATING_LINK'), (3, 'MARKED_AS_DUPLICATE'), (4, 'UPDATED_LINK'), (5, 'CRAWLING'), (6, 'CRAWLING_FAILED'), (7, 'RESCHEDULED_LONG_CRAWLING'), (8, 'CRAWLING_TOO_LONG'), (9, 'HAS_NO_PAGES'), (10, 'TEXT_UPLOADED'), (11, 'AWAITING_CRAWL'), (12, 'INDEXED_BY_ELASTIC'), (13, 'TEXT_ANALYZED'), (14, 'DOMAIN_INVALID'), (15, 'NO_LINKS_IN_PAGE'), (16, 'UNCRAWLABLE')], default=notifier.consts.CRAWLING_STATUSES['NOT_CRAWLED'], max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blacklisted', models.BooleanField(default=False)),
                ('last_crawled', models.DateTimeField(default=None, null=True)),
                ('employees_min', models.PositiveIntegerField(blank=True, default=1)),
                ('employees_max', models.PositiveIntegerField(blank=True, default=1)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
            bases=(models.Model, notifier.models.Entity),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('crawling_status', models.CharField(choices=[(0, 'NOT_CRAWLED'), (1, 'ERROR_REQUESTING_LINK'), (2, 'UPDATING_LINK'), (3, 'MARKED_AS_DUPLICATE'), (4, 'UPDATED_LINK'), (5, 'CRAWLING'), (6, 'CRAWLING_FAILED'), (7, 'RESCHEDULED_LONG_CRAWLING'), (8, 'CRAWLING_TOO_LONG'), (9, 'HAS_NO_PAGES'), (10, 'TEXT_UPLOADED'), (11, 'AWAITING_CRAWL'), (12, 'INDEXED_BY_ELASTIC'), (13, 'TEXT_ANALYZED'), (14, 'DOMAIN_INVALID'), (15, 'NO_LINKS_IN_PAGE'), (16, 'UNCRAWLABLE')], default=notifier.consts.CRAWLING_STATUSES['NOT_CRAWLED'], max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blacklisted', models.BooleanField(default=False)),
                ('last_crawled', models.DateTimeField(default=None, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, notifier.models.Entity),
        ),
        migrations.CreateModel(
            name='Webinar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('crawling_status', models.CharField(choices=[(0, 'NOT_CRAWLED'), (1, 'ERROR_REQUESTING_LINK'), (2, 'UPDATING_LINK'), (3, 'MARKED_AS_DUPLICATE'), (4, 'UPDATED_LINK'), (5, 'CRAWLING'), (6, 'CRAWLING_FAILED'), (7, 'RESCHEDULED_LONG_CRAWLING'), (8, 'CRAWLING_TOO_LONG'), (9, 'HAS_NO_PAGES'), (10, 'TEXT_UPLOADED'), (11, 'AWAITING_CRAWL'), (12, 'INDEXED_BY_ELASTIC'), (13, 'TEXT_ANALYZED'), (14, 'DOMAIN_INVALID'), (15, 'NO_LINKS_IN_PAGE'), (16, 'UNCRAWLABLE')], default=notifier.consts.CRAWLING_STATUSES['NOT_CRAWLED'], max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blacklisted', models.BooleanField(default=False)),
                ('last_crawled', models.DateTimeField(default=None, null=True)),
                ('link', models.URLField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('language', models.CharField(default='en', max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, notifier.models.Entity),
        ),
        migrations.CreateModel(
            name='ContentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('crawling_status', models.CharField(choices=[(0, 'NOT_CRAWLED'), (1, 'ERROR_REQUESTING_LINK'), (2, 'UPDATING_LINK'), (3, 'MARKED_AS_DUPLICATE'), (4, 'UPDATED_LINK'), (5, 'CRAWLING'), (6, 'CRAWLING_FAILED'), (7, 'RESCHEDULED_LONG_CRAWLING'), (8, 'CRAWLING_TOO_LONG'), (9, 'HAS_NO_PAGES'), (10, 'TEXT_UPLOADED'), (11, 'AWAITING_CRAWL'), (12, 'INDEXED_BY_ELASTIC'), (13, 'TEXT_ANALYZED'), (14, 'DOMAIN_INVALID'), (15, 'NO_LINKS_IN_PAGE'), (16, 'UNCRAWLABLE')], default=notifier.consts.CRAWLING_STATUSES['NOT_CRAWLED'], max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blacklisted', models.BooleanField(default=False)),
                ('last_crawled', models.DateTimeField(default=None, null=True)),
                ('link', models.CharField(max_length=255, unique=True)),
                ('snippet', models.CharField(blank=True, max_length=255)),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='notifier.company')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, notifier.models.Entity),
        ),
        migrations.CreateModel(
            name='CompanyForWebinar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blacklisted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifier.company')),
                ('webinar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifier.webinar')),
            ],
            bases=(models.Model, notifier.models.Entity),
        ),
        migrations.CreateModel(
            name='CompanyForEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(blank=True, default=False)),
                ('is_blacklisted', models.BooleanField(blank=True, default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifier.company')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifier.event')),
            ],
            bases=(models.Model, notifier.models.Entity),
        ),
        migrations.CreateModel(
            name='CompanyCompetitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='notifier.company')),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitor', to='notifier.company')),
            ],
            bases=(models.Model, notifier.models.Entity),
        ),
    ]
