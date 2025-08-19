from rest_framework import serializers
from .models import Library, Book, Author, Category, Member, Borrowing, Review

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    #authors_first_name=serializers.CharField(source="author.first_name",read_only=True)
    author_full_name = serializers.SerializerMethodField()
    #authors_last_name=serializers.CharField(source="author.last_name",read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    @staticmethod
    def get_author_full_name(obj):
        return ", ".join(
            f"{author.first_name} {author.last_name}" for author in obj.authors.all()
        )

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
