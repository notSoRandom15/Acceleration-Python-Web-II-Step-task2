from typing import Any
from django.db import models
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Book, BookRequest
from django.views.generic.edit import CreateView, UpdateView
from .forms import BookForm
from .filters import BookFilter
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse




class BookListView(ListView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = 'book_list'
    template_name = 'books/book_list.html'
    login_url = 'account_login' # we use account_login cause we have django-allauth so it knows automatically

    def get_queryset(self) -> QuerySet[Any]:
        queryset =  super().get_queryset()
        self.filterset = BookFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'
    login_url = 'account_login'
    permission_required = 'books.special_status'
    queryset = Book.objects.all().prefetch_related('reviews__author') 

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        book = self.get_object()
        user = self.request.user

        if user != book.uploaded_by:
            if BookRequest.objects.filter(book=book, user=user, fulfilled=False).exists():
                context['already_requested'] = True
            else:
                context['can_request'] = True

        return context
    
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        user = self.request.user

        # Check if the user can request the book
        if user != book.author and not BookRequest.objects.filter(book=book, user=user, fulfilled=False).exists():
            BookRequest.objects.create(book=book, user=user)
            messages.success(request, f"You have requested '{book}' successfully!")

        return self.get(request, *args, **kwargs)
class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'
    # queryset = Book.objects.filter(title__icontains='beginners')

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)
    


class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_update.html"
    success_url = reverse_lazy('book_list')

    def get_queryset(self):
        return Book.objects.filter(pk=self.kwargs['pk'])
    



class AuthorRequestListView(ListView):
    model = BookRequest
    template_name = 'books/author_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        user = self.request.user
        return BookRequest.objects.filter(book__uploaded_by=user, fulfilled=False) 
    




def accept_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            book_request.fulfilled = True
            book_request.save()
            messages.success(request, f"Your request for '{book_request.book.title}' accepted successfully!")
        elif action == 'decline':
            book_request.delete()
            messages.info(request, f"your request for '{book_request.book.title}' has been declined.")
    
    return redirect(reverse('book_detail', kwargs={'pk': book_request.book.pk}))
