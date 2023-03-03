from django.db import models

class Roll(models.Model):
    tag    = models.SlugField()
    length = models.DecimalField(unique=True, decimal_places=2, max_digits=3)
    quantity = models.PositiveSmallIntegerField(default=1, blank=True)
    
    def __str__(self):
        return f"Roll[{slug}: {self.quantity}, {self.length}]"

class Cut(models.Model):
    length = models.DecimalField(unique=True, decimal_places=2, max_digits=3)
    quantity = models.PositiveSmallIntegerField(default=1, blank=True)

    def __str__(self):
        return f"Order[{self.quantity}, {self.length}]"

class CutOrder():
    pass
