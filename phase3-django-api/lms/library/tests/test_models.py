from django.test import TestCase
from ..models import Author, Category, Book

class AuthorModelTest(TestCase):
    def test_author_creation(self):
        author = Author.objects.create(
            first_name="J.K.",
            last_name="Rowling",
            nationality="British"
        )
        self.assertEqual(str(author), "J.K. Rowling")


class BookModelTest(TestCase):
    def test_book_creation_with_author_and_category(self):
        author = Author.objects.create(
            first_name="George",
            last_name="Orwell",
            nationality="British"
        )
        category = Category.objects.create(name="Dystopian")

        book = Book.objects.create(
            title="1984",
            total_copies=10,
            available_copies=5,
        )
        book.authors.add(author)
        book.categories.add(category)

        self.assertEqual(str(book), "1984")
        self.assertIn(author, book.authors.all())
        self.assertIn(category, book.categories.all())
