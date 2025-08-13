from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LibraryViewSet, BookViewSet, AuthorViewSet, CategoryViewSet,
    MemberViewSet, BorrowingViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'libraries', LibraryViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'members', MemberViewSet)
router.register(r'borrowings', BorrowingViewSet)
router.register(r'reviews', ReviewViewSet)


book_borrow = BookViewSet.as_view({"post": "borrow"})
urlpatterns = [
    path('', include(router.urls)),
]
