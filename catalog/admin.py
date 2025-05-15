from django.contrib import admin
from .models import Author, Book, Borrower, Loan

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date')
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'isbn')
    list_filter = ('author', 'genre', 'language')
    search_fields = ('title', 'summary', 'isbn')
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'summary')
        }),
        ('Details', {
            'fields': ('isbn', 'genre', 'language', 'cover_image'),
            'classes': ('collapse',)
        }),
    )
    
    def display_genre(self, obj):
        return obj.genre
    display_genre.short_description = 'Genre'

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'loan_date', 'return_date', 'is_overdue')
    list_filter = ('loan_date', 'returned')
    search_fields = ('book__title', 'borrower__name')
    date_hierarchy = 'loan_date'
    
    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'