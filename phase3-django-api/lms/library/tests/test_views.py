from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from ..models import Author, Category, Book, Borrowing, Review, Member


class AuthorAPITestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="George", last_name="Orwell", nationality="British"
        )
        self.url = reverse("author-list")

    def test_list_authors(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_author(self):
        response = self.client.post(
            self.url, {"first_name": "J.K.", "last_name": "Rowling", "nationality": "British"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fiction")
        self.url = reverse("category-list")

    def test_list_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        response = self.client.post(self.url, {"name": "Science"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="George", last_name="Orwell", nationality="British")
        self.category = Category.objects.create(name="Dystopian")
        self.book = Book.objects.create(title="1984", total_copies=10, available_copies=5)
        self.book.authors.add(self.author)
        self.book.categories.add(self.category)
        self.url = reverse("book-list")

    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        response = self.client.post(
            self.url,
            {
                "title": "Animal Farm",
                "total_copies": 8,
                "available_copies": 8,
                "authors": [self.author.pk],
                "categories": [self.category.pk],
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)


class MemberBorrowingReviewAPITestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Agatha", last_name="Christie", nationality="British")
        self.category = Category.objects.create(name="Mystery")
        self.book = Book.objects.create(title="Murder on the Orient Express", total_copies=5, available_copies=5)
        self.book.authors.add(self.author)
        self.book.categories.add(self.category)

        self.member = Member.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            member_type="Student",
            registration_date=date.today(),
        )

        self.borrowing_url = reverse("borrowing-list")
        self.review_url = reverse("review-list")

    def test_create_borrowing(self):
        response = self.client.post(
            self.borrowing_url,
            {"book": self.book.pk, "member": self.member.pk, "borrow_date": date.today()},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)

    def test_list_borrowings(self):
        Borrowing.objects.create(book=self.book, member=self.member, borrow_date=date.today())
        response = self.client.get(self.borrowing_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_review(self):
        response = self.client.post(
            self.review_url,
            {"book": self.book.pk, "member": self.member.pk, "rating": 5, "review_date": date.today()},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_list_reviews(self):
        Review.objects.create(book=self.book, member=self.member, rating=4, review_date=date.today())
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
