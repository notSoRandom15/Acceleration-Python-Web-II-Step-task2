import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Book(models.Model):
    id = models.UUIDField(primary_key=True,
                    default=uuid.uuid4,
                    editable=False
                          )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    cover = models.ImageField(upload_to='covers/', blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]
        
        permissions = [
            ('special_status', 'can_read_all_books'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
        

class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    review = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review
    

class BookRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fulfilled = models.BooleanField(default=False)