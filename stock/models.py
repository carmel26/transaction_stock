from django.db import models

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom

class Transaction(models.Model):
    ENTREE = 'ENT'
    SORTIE = 'SOR'
    TYPE_CHOICES = [
        (ENTREE, 'Entrée'),
        (SORTIE, 'Sortie'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    quantite = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.produit.nom} - {self.quantite}"
