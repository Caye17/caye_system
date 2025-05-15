from rest_framework import serializers
from .models import Book, Author, Loan, Borrower

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()  # or `author = serializers.StringRelatedField()`

    class Meta:
        model = Book
        fields = '__all__'

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    borrower = BorrowerSerializer()

    class Meta:
        model = Loan
        fields = '__all__'
