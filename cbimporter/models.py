from django.db import models
from django.utils import timezone
import cbpro
import os

auth_client = cbpro.AuthenticatedClient(
	os.environ['CB_KEY'],
	os.environ['B64SECRET'],
	os.environ['PASSPHRASE']
)

class Portfolio(models.Model):
	updated_at = models.DateTimeField(auto_now=True)
	total_value = models.DecimalField(max_digits=8, decimal_places=2)
	high_date = models.DateTimeField()
	high_value = models.DecimalField(max_digits=8, decimal_places=2)

class Account(models.Model):
	portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
	cb_id = models.CharField(max_length=36, unique=True)
	currency = models.CharField(max_length=4)
	quantity = models.DecimalField(max_digits=25, decimal_places=16)
	available = models.DecimalField(max_digits=25, decimal_places=16)
	hold = models.DecimalField(max_digits=25, decimal_places=16)
	price = models.DecimalField(max_digits=16, decimal_places=8)
	value = models.DecimalField(max_digits=16, decimal_places=8)