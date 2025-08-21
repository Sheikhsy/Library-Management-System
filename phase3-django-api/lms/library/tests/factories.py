# library/tests/factories.py
import factory
from ..models import Author, Book, Member, Borrowing, Review
from django.contrib.auth.models import User
import datetime

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker("name")
    birth_date = factory.Faker("date_of_birth")

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=3)
    published_date = factory.Faker("date")
    author = factory.SubFactory(AuthorFactory)
    category = "Fiction"

class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    name = factory.Faker("name")
    email = factory.Faker("email")
    membership_type = "student"

class BorrowingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Borrowing

    book = factory.SubFactory(BookFactory)
    member = factory.SubFactory(MemberFactory)
    borrowed_date = factory.LazyFunction(datetime.date.today)

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    book = factory.SubFactory(BookFactory)
    member = factory.SubFactory(MemberFactory)
    rating = 4
    comment = factory.Faker("sentence")
