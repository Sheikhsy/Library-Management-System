# library/tests/test_integration.py
import pytest
from django.urls import reverse
from .factories import AuthorFactory, BookFactory, MemberFactory

@pytest.mark.django_db
def test_book_lifecycle(auth_client):
    client, _ = auth_client
    author = AuthorFactory()

    # Create
    create_url = reverse("book-list")
    response = client.post(create_url, {
        "title": "Test Driven Dev",
        "author": author.id,
        "published_date": "2025-01-01",
        "category": "Tech"
    }, format="json")
    assert response.status_code == 201
    book_id = response.data["id"]

    # Retrieve
    detail_url = reverse("book-detail", args=[book_id])
    response = client.get(detail_url)
    assert response.status_code == 200
    assert response.data["title"] == "Test Driven Dev"

    # Update
    response = client.patch(detail_url, {"title": "Updated Title"}, format="json")
    assert response.status_code == 200
    assert response.data["title"] == "Updated Title"

    # Delete
    response = client.delete(detail_url)
    assert response.status_code == 204
