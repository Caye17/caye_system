from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'loans', views.LoanViewSet)
router.register(r'borrowers', views.BorrowerViewSet)

urlpatterns = [
    # Dashboard as homepage
    path('', views.DashboardView.as_view(), name='home'),

    # Book HTML pages
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),

    # Author HTML pages
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),

    # Borrower HTML pages
    path('borrowers/', views.BorrowerListView.as_view(), name='borrowers'),
    path('borrower/<int:pk>/', views.BorrowerDetailView.as_view(), name='borrower-detail'),
    path('borrower/create/', views.BorrowerCreateView.as_view(), name='borrower-create'),
    path('borrower/<int:pk>/update/', views.BorrowerUpdateView.as_view(), name='borrower-update'),
    path('borrower/<int:pk>/delete/', views.BorrowerDeleteView.as_view(), name='borrower-delete'),

    # Loan HTML pages
    path('loans/', views.LoanListView.as_view(), name='loans'),
    path('loan/<int:pk>/', views.LoanDetailView.as_view(), name='loan-detail'),
    path('loan/create/', views.LoanCreateView.as_view(), name='loan-create'),
    path('loan/<int:pk>/update/', views.LoanUpdateView.as_view(), name='loan-update'),
    path('loan/<int:pk>/delete/', views.LoanDeleteView.as_view(), name='loan-delete'),

    # API routes
    path('api/', include(router.urls)),
]
