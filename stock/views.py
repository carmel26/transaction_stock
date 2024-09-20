from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import Produit, Transaction
from .forms import TransactionForm

class ProduitListView(ListView):
    model = Produit
    template_name = 'stock/produit_list.html'
    context_object_name = 'produits'
    paginate_by = 10  # Nombre de produits par page

class ProduitDetailView(DetailView):
    model = Produit
    template_name = 'stock/produit_detail.html'
    context_object_name = 'produit'

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'stock/transaction_form.html'
    success_url = reverse_lazy('stock:produit_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_type = self.kwargs.get('type')
        if transaction_type == 'entree':
            context['transaction_type'] = 'ENT'
            context['transaction_type_display'] = 'Entrée'
        elif transaction_type == 'sortie':
            context['transaction_type'] = 'SOR'
            context['transaction_type_display'] = 'Sortie'
        else:
            context['transaction_type'] = None
        return context

    def form_valid(self, form):
        transaction_type = self.kwargs.get('type')
        if transaction_type not in ['entree', 'sortie']:
            messages.error(self.request, 'Type de transaction invalide.')
            return self.form_invalid(form)

        transaction = form.save(commit=False)
        if transaction_type == 'entree':
            transaction.type = Transaction.ENTREE
            transaction_type_display = 'Entrée'
        elif transaction_type == 'sortie':
            transaction.type = Transaction.SORTIE
            transaction_type_display = 'Sortie'

        produit = transaction.produit
        if transaction.type == Transaction.ENTREE:
            produit.quantite += transaction.quantite
        elif transaction.type == Transaction.SORTIE:
            if produit.quantite >= transaction.quantite:
                produit.quantite -= transaction.quantite
            else:
                form.add_error('quantite', 'Quantité insuffisante en stock.')
                return self.form_invalid(form)
        produit.save()
        transaction.save()
        messages.success(self.request, f'Transaction de {transaction_type_display} enregistrée avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de l\'enregistrement de la transaction.')
        return super().form_invalid(form)
