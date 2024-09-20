from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['produit', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={"class": "form-select"}),
            'quantite': forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Supprimer le champ type du formulaire
        if 'type' in self.fields:
            del self.fields['type']
