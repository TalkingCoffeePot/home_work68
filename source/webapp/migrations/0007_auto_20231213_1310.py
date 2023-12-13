# Generated by Django 4.2.7 on 2023-12-13 13:10

from django.db import migrations


def transfer_tags(apps, schema_editor):
    Article = apps.get_model('webapp.Article')
    for article in Article.objects.all():
        article.tags.set(article.old_tags.all())


def rollback_transfer(apps, schema_editor):
    Article = apps.get_model('webapp.Article')
    for article in Article.objects.all():
        article.old_tags.set(article.tags.all())


class Migration(migrations.Migration):
    dependencies = [
        ('webapp', '0006_article_tags'),
    ]

    operations = [
        migrations.RunPython(transfer_tags, rollback_transfer)
    ]
