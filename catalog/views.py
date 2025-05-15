from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from .models import Author, Book, Borrower, Loan
from .forms import AuthorForm, BookForm, BorrowerForm, LoanForm
from rest_framework import viewsets, filters
from .serializers import AuthorSerializer, BookSerializer, LoanSerializer, BorrowerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.db.models import Q
from django.views.generic import ListView

# === Mixin for Success Message ===
class SuccessMessageMixin:
    def form_valid(self, form):
        messages.success(self.request, f"{self.model._meta.verbose_name.title()} successfully deleted!")
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f"{self.model._meta.verbose_name.title()} deleted successfully!")
        return super().delete(request, *args, **kwargs)


# === DASHBOARD VIEW ===
class DashboardView(TemplateView):
    template_name = 'catalog/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total counts
        context['total_books'] = Book.objects.count()
        context['total_authors'] = Author.objects.count()
        context['total_borrowers'] = Borrower.objects.count()
        context['total_loans'] = Loan.objects.count()

        # Active and returned loans
        context['active_loans'] = Loan.objects.filter(returned=False).count()
        context['returned_loans'] = Loan.objects.filter(returned=True).count()

        # Get borrowers and their total loans
        borrowers = Borrower.objects.all()
        loans_per_borrower = []
        for borrower in borrowers:
            loans_per_borrower.append({
                'borrower': borrower,
                'loan_count': borrower.get_total_loans(),
            })
        context['loans_per_borrower'] = loans_per_borrower

        return context


# === AUTHOR VIEWS ===
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'
    paginate_by = 10


class AuthorCreateView(SuccessMessageMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'catalog/author_form.html'
    success_url = reverse_lazy('authors')
    action = "Author added successfully."


class AuthorUpdateView(SuccessMessageMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'catalog/author_form.html'
    success_url = reverse_lazy('authors')
    action = "updaAuthor updated successfully"


class AuthorDeleteView(SuccessMessageMixin, DeleteView):
    model = Author
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('authors')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse_lazy('authors')
        return context


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'
    context_object_name = 'author'


# === BOOK VIEWS ===
class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'books'
    paginate_by = 9

    def get_queryset(self):
        queryset = Book.objects.all().order_by('title')

        # Search filter
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(author__first_name__icontains=search_query) |
                Q(author__last_name__icontains=search_query)
            )

        # Author filter
        author_filter = self.request.GET.get('author', '').strip()
        if author_filter:
            queryset = queryset.filter(author__last_name__iexact=author_filter)

        # Genre filter (string match)
        genre_filter = self.request.GET.get('genre', '').strip()
        if genre_filter:
            queryset = queryset.filter(genre__iexact=genre_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all().order_by('last_name')
        context['genres'] = Book.objects.values_list('genre', flat=True).distinct().order_by('genre')
        return context



class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['genres'] = Book.objects.values_list('genre', flat=True).distinct()
        return context


class BookCreateView(SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'catalog/book_form.html'
    success_url = reverse_lazy('home')
    action = "added"  # Set action to 'added' for create view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = self.action  # Pass action to template for 'Create'
        context['title'] = "Add Book"  # Set title to Add Book for create
        return context


class BookUpdateView(SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'catalog/book_form.html'
    success_url = reverse_lazy('books')
    action = "updated"  # Set action to 'updated' for update view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = self.action  # Pass action to template for 'Update'
        context['title'] = "Edit Book"  # Set title to Edit Book for update
        return context


class BookDeleteView(SuccessMessageMixin, DeleteView):
    model = Book
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('books')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse_lazy('books')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Successfully deleted: {self.object.title}')
        return super().form_valid(form)

# === BORROWER VIEWS ===
class BorrowerListView(generic.ListView):
    model = Borrower
    template_name = 'catalog/borrower_list.html'
    context_object_name = 'borrowers'
    paginate_by = 10


class BorrowerDetailView(generic.DetailView):
    model = Borrower
    template_name = 'catalog/borrower_detail.html'
    context_object_name = 'borrower'


class BorrowerCreateView(SuccessMessageMixin, CreateView):
    model = Borrower
    form_class = BorrowerForm
    template_name = 'catalog/borrower_form.html'
    success_url = reverse_lazy('borrowers')
    action = "Borrower added successfully."


class BorrowerUpdateView(SuccessMessageMixin, UpdateView):
    model = Borrower
    form_class = BorrowerForm
    template_name = 'catalog/borrower_form.html'
    success_url = reverse_lazy('borrowers')
    action = "Borrower updated successfully."


class BorrowerDeleteView(SuccessMessageMixin, DeleteView):
    model = Borrower
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('borrowers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse_lazy('borrowers')
        return context

# === LOAN VIEWS ===
class LoanListView(generic.ListView):
    model = Loan
    template_name = 'catalog/loan_list.html'
    context_object_name = 'loans'
    paginate_by = 10


class LoanDetailView(generic.DetailView):
    model = Loan
    template_name = 'catalog/loan_detail.html'
    context_object_name = 'loan'


class LoanCreateView(SuccessMessageMixin, CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'catalog/loan_form.html'
    success_url = reverse_lazy('loans')
    action = "Loan added successfully."


class LoanUpdateView(SuccessMessageMixin, UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'catalog/loan_form.html'
    success_url = reverse_lazy('loans')
    action = "Loan updated successfully."


class LoanDeleteView(SuccessMessageMixin, DeleteView):
    model = Loan
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('loans')  # Change if your loan list view uses another name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = reverse_lazy('loans')
        return context


# === API ViewSets ===
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'genre', 'language']
    search_fields = ['title', 'summary']
    ordering_fields = ['title', 'publication_date']


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['borrower__first_name', 'book__title']
    ordering_fields = ['loan_date']


class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']
