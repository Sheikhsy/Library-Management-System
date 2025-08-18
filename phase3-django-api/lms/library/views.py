from django.db.models.functions import Trunc
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters,status
from rest_framework.decorators import action


from .models import Library, Book, Author, Category, Member, Borrowing, Review
from .serializers import (
    LibrarySerializer, BookSerializer, AuthorSerializer, CategorySerializer,
    MemberSerializer, BorrowingSerializer, ReviewSerializer
)
from django.utils import timezone
from rest_framework.response import Response
from django.db.models import Count
from django.utils.timezone import now
from django.db.models import Value, F
from django.db.models.functions import Concat
from drf_yasg import openapi


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_summary="List all Libraries",
        operation_description="Returns a paginated list of Libraries.",
        responses={200: LibrarySerializer(many=True)}
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_summary="Get a single Library",
        operation_description="Retrieve detailed information about a single Library by ID.",
        responses={200: LibrarySerializer()}
    )
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_summary="Create a new member",
        request_body=LibrarySerializer,
        responses={201: LibrarySerializer()}
    )
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        operation_summary="Update a Library",
        request_body=LibrarySerializer,
        responses={200: LibrarySerializer()}
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_summary="Partially update a Library",
        request_body=LibrarySerializer,
        responses={200: LibrarySerializer()}
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_summary="Delete a Library",
        responses={204: 'No Content'}
    )
)
class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'campus_location','library_id']
    ordering_fields = ['name', 'library_id']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['book_id','title','authors__first_name','authors__last_name','categories__name']
    ordering_fields = ['title', 'book_id']


    @action(detail=True,methods=["get"])
    def availability(self,request,pk=None):
        book=self.get_object()
        try:
            book = self.get_object()  # fetch the Book by pk
            data = {
                "book_id": book.book_id,
                "title": book.title,
                "total_copies": book.total_copies,
                "available_copies": book.available_copies,
                "is_available": book.available_copies > 0
            }
            return Response(data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)




class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name']
    ordering_fields = ['category_id']



@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_summary="List all members",
        operation_description="Returns a paginated list of members.",
        responses={200: MemberSerializer(many=True)}
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_summary="Get a single member",
        operation_description="Retrieve detailed information about a single member by ID.",
        responses={200: MemberSerializer()}
    )
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_summary="Create a new member",
        request_body=MemberSerializer,
        responses={201: MemberSerializer()}
    )
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        operation_summary="Update a member",
        request_body=MemberSerializer,
        responses={200: MemberSerializer()}
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_summary="Partially update a member",
        request_body=MemberSerializer,
        responses={200: MemberSerializer()}
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_summary="Delete a member",
        responses={204: 'No Content'}
    )
)
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    @action(detail=True, methods=['get'])
    def borrowings(self, request, pk=None):
        # Get the member object by ID (pk)
        member = self.get_object()
        borrowings = Borrowing.objects.filter(member=member).order_by('-borrow_date')
        serializer = BorrowingSerializer(borrowings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    @action(detail=False, methods=['post'], url_path='borrow')
    def borrow(self, request):
        book_id = request.data.get('book_id')
        member_id = request.data.get('member_id')

        if not book_id or not member_id:
            return Response({"error": "Both book_id and member_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if book is
        #
        # available (available_copies > 0)
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        if book.available_copies <= 0:
            return Response({"error": "No copies available for this book."}, status=status.HTTP_400_BAD_REQUEST)
        # In your borrow action

        if Borrowing.objects.filter(book_id=book_id, member_id=member_id, returned=False).exists():
            return Response({"error": "You already have this book borrowed. Return it before borrowing again."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if member exists
        try:
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create borrowing record
        borrowing = Borrowing.objects.create(
            book=book,
            member=member,
            borrow_date=timezone.now(),
            due_date=timezone.now() + timezone.timedelta(days=30),
            returned=False
        )

        # Decrement available copies
        book.total_copies -= 1
        book.available_copies -= 1
        book.save()

        serializer = BorrowingSerializer(borrowing)
        return Response({"message":"Book has been Borrowed Successfully","data":serializer.data},
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='return')
    def return_book(self, request):
        book_id = request.data.get('book_id')
        member_id = request.data.get('member_id')

        if not book_id or not member_id:
            return Response({"error": "book_id and member_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            borrowing = Borrowing.objects.get(
                book_id=book_id,
                member_id=member_id,
                returned=False
            )
        except Borrowing.DoesNotExist:
            return Response({"error": "No active borrowing found for this book and member."},
                            status=status.HTTP_404_NOT_FOUND)

        borrowing.returned = True
        borrowing.return_date = timezone.now()

        if borrowing.due_date and borrowing.return_date.date() > borrowing.due_date:
            days_late = (borrowing.return_date.date() - borrowing.due_date).days
            borrowing.late_fee = days_late * 30  # 30 currency units per day late
        else:
            borrowing.late_fee = 0

        borrowing.save()

        # Increase available copies in book
        book = borrowing.book
        book.available_copies += 1
        book.total_copies += 1
        book.save()

        serializer = BorrowingSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        today = now().date()

        total_books = Book.objects.count()
        total_members = Member.objects.count()
        total_borrowings = Borrowing.objects.count()
        books_borrowed_now = Borrowing.objects.filter(returned=False).count()
        overdue_books = Borrowing.objects.filter(due_date__lt=today, returned=False).count()

        most_borrowed_book = (
            Borrowing.objects
            .values('book__title')
            .annotate(count=Count('borrowing_id'))
            .order_by('-count')
            .first()
        )

        most_active_member = (
            Borrowing.objects
            .values(full_name=Concat(F('member__first_name'), Value(' '), F('member__last_name')))
            .annotate(count=Count('borrowing_id'))
            .order_by('-count')
            .first()
        )

        stats = {
            "total_books": total_books,
            "total_members": total_members,
            "total_borrowings": total_borrowings,
            "books_borrowed_now": books_borrowed_now,
            "overdue_books": overdue_books,
            "most_borrowed_book": most_borrowed_book['book__title'] if most_borrowed_book else None,
            "most_active_member": most_active_member['full_name'] if most_active_member else None,
        }

        return Response(stats)



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
