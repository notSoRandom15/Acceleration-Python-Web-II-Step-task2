from django import forms
from .models import Book, BookRequest

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'price', 'location', 'cover' ]

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'price', 'location','cover']

class BookRequestForm(forms.ModelForm):
    class Meta: 
        model = BookRequest
        fields = ['book']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(bookrequest__fulfilled=False)
        self.fields['book'].empty_label = None
        self.fields['book'].label = 'Select a Book'