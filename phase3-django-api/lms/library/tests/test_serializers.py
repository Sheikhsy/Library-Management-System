# library/tests/test_serializers.py
import pytest
from ..serializers import AuthorSerializer, BookSerializer
from .factories import AuthorFactory, BookFactory

@pytest.mark.django_db
def test_author_serializer():
    author = AuthorFactory(first_name="George Orwell")
    data = AuthorSerializer(author).data
    assert data["first_name"] == "George Orwell"

@pytest.mark.django_db
def test_book_serializer():
    book = BookFactory(title="1984")
    data = BookSerializer(book).data
    assert data["title"] == "1984"
    assert "author" in data
