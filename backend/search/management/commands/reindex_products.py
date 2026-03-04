from django.core.management.base import BaseCommand
from products.models import Product
from search.services import MeilisearchService, product_to_search_document


class Command(BaseCommand):
    help = 'Reindex all products in Meilisearch'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear index before reindexing',
        )
    
    def handle(self, *args, **options):
        search_service = MeilisearchService()
        
        if options['clear']:
            self.stdout.write('Clearing existing index...')
            search_service.clear_index()
            self.stdout.write(self.style.SUCCESS('✓ Index cleared'))
        
        self.stdout.write('Fetching products...')
        products = Product.objects.filter(
            is_active=True
        ).select_related(
            'category', 'vendor'
        ).prefetch_related('images', 'variants')
        
        total = products.count()
        self.stdout.write(f'Found {total} active products')
        
        if total == 0:
            self.stdout.write(self.style.WARNING('No products to index'))
            return
        
        self.stdout.write('Indexing products...')
        documents = [product_to_search_document(p) for p in products]
        
        try:
            search_service.index_products_bulk(documents)
            self.stdout.write(self.style.SUCCESS(f'✓ Successfully indexed {total} products'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
