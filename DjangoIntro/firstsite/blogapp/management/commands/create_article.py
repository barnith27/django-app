from django.core.management import BaseCommand
from django.db import transaction
from blogapp.models import Article, Author, Category, Tag

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Create article')
        author, created = Author.objects.get_or_create(
            name='Кристина Брусник',
            defaults={'bio': 'Биография автора'}
        )

        category, created = Category.objects.get_or_create(
            name='Технологии'
        )

        tag1, created = Tag.objects.get_or_create(name='Python')
        tag2, created = Tag.objects.get_or_create(name='Django')

        article = Article.objects.create(
            title='Моя первая статья',
            content='Содержание статьи...',
            author=author,
            category=category
        )

        article.tags.add(tag1, tag2)

        self.stdout.write(f'Created article: {article.title}')