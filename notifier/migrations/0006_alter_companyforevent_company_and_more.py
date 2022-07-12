# Generated by Django 4.0.6 on 2022-07-11 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0005_alter_companyforevent_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyforevent',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_events', to='notifier.company'),
        ),
        migrations.AlterField(
            model_name='companyforevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_companies', to='notifier.event'),
        ),
        migrations.AlterField(
            model_name='companyforwebinar',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_webinars', to='notifier.company'),
        ),
        migrations.AlterField(
            model_name='companyforwebinar',
            name='webinar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webinar_companies', to='notifier.webinar'),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_content_items', to='notifier.company'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]