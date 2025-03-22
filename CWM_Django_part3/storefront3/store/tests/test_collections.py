from rest_framework.test import APITClient
from rest_framework import status


class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
        # Arange
        
        # Act
        client = APITClient()
        response = client.post('/store/collections/', {'title': 'a'})
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED