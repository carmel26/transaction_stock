from django.contrib import admin
from .models import Produit, Transaction

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'quantite')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'produit', 'quantite', 'date')
    list_filter = ('type', 'produit')
