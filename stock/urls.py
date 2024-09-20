from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.ProduitListView.as_view(), name='produit_list'),
    path('produit/<int:pk>/', views.ProduitDetailView.as_view(), name='produit_detail'),
    path('transaction/<str:type>/', views.TransactionCreateView.as_view(), name='transaction'),
]
