from django.urls import path
from .views import BookListView, BookDetailView, SearchResultsListView, BookCreateView, BookUpdateView, AuthorRequestListView, accept_request

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<uuid:pk>', BookDetailView.as_view(), name='book_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path("book_form/", BookCreateView.as_view(), name="book_form"),
    path("book_update/<uuid:pk>", BookUpdateView.as_view(), name="book_update"),
    path("author_requests/", AuthorRequestListView.as_view(), name="author_requests"),
    path("accept_request/<int:pk>/", accept_request, name="accept_request"),
]
