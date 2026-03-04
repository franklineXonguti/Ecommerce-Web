from django.core.management.base import BaseCommand
from search.services import MeilisearchService


class Command(BaseCommand):
    help = 'Configure Meilisearch index settings'
    
    def handle(self, *args, **options):
        self.stdout.write('Configuring Meilisearch index...')
        
        try:
            search_service = MeilisearchService()
            search_service.configure_index()
            
            self.stdout.write(self.style.SUCCESS('✓ Search index configured successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
