import pytest
from recommendations.models import UserEvent
from recommendations.services import RecommendationEngine


@pytest.fixture
def user_event(db, user, product):
    """Fixture for creating a user event"""
    return UserEvent.objects.create(
        user=user,
        product=product,
        event_type='VIEW'
    )


@pytest.mark.django_db
class TestUserEventModel:
    """Test UserEvent model"""
    
    def test_user_event_creation(self, user_event, user, product):
        """Test user event is created successfully"""
        assert user_event.user == user
        assert user_event.product == product
        assert user_event.event_type == 'VIEW'


@pytest.mark.django_db
class TestRecommendationEngine:
    """Test recommendation engine"""
    
    def test_get_recommendations_for_new_user(self, user, product):
        """Test recommendations for user with no history"""
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(user, limit=5)
        
        # Should return trending products for new users
        assert isinstance(recommendations, list)
    
    def test_track_event(self, user, product):
        """Test tracking user events"""
        engine = RecommendationEngine()
        engine.track_event(user, product, 'VIEW')
        
        assert UserEvent.objects.filter(
            user=user,
            product=product,
            event_type='VIEW'
        ).exists()
