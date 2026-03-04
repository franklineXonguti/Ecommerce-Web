import pytest
from unittest.mock import patch, MagicMock
from search.services import MeilisearchService


@pytest.mark.django_db
class TestMeilisearchService:
    """Test Meilisearch service"""
    
    @patch('meilisearch.Client')
    def test_index_product(self, mock_client, product):
        """Test indexing a product"""
        mock_index = MagicMock()
        mock_client.return_value.index.return_value = mock_index
        
        service = MeilisearchService()
        service.index_product(product)
        
        mock_index.add_documents.assert_called_once()
    
    @patch('meilisearch.Client')
    def test_search_products(self, mock_client):
        """Test searching products"""
        mock_index = MagicMock()
        mock_index.search.return_value = {
            'hits': [
                {'id': 1, 'name': 'Test Product', 'price_kes': 1000}
            ],
            'estimatedTotalHits': 1
        }
        mock_client.return_value.index.return_value = mock_index
        
        service = MeilisearchService()
        results = service.search('test', limit=10)
        
        assert len(results['hits']) == 1
        assert results['hits'][0]['name'] == 'Test Product'
        mock_index.search.assert_called_once()
