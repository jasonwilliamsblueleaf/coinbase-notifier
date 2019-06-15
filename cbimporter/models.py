from django.db import models
from django.utils import timezone
from django.db.models import Sum
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

	def import_new_accounts(self):
		response = auth_client.get_accounts()
		stored_accounts = Portfolio.objects.first().account_set.all()
		for account in response:
			if stored_accounts.filter(cb_id=account['id']).count() == 0 and float(account['balance']) != 0:
				self.account_set.create(
					cb_id = account['id'],
					currency = account['currency'],
					quantity = account['balance'],
					available = account['available'],
					hold = account['hold'],
					price = 0,
					value = 0
					)

	def update_total_value(self):
		accounts = self.account_set.all()
		self.total_value = accounts.aggregate(total_value = Sum('value'))['total_value']
		self.save()

class Account(models.Model):
	portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
	cb_id = models.CharField(max_length=36, unique=True)
	currency = models.CharField(max_length=4)
	quantity = models.DecimalField(max_digits=25, decimal_places=16)
	available = models.DecimalField(max_digits=25, decimal_places=16)
	hold = models.DecimalField(max_digits=25, decimal_places=16)
	price = models.DecimalField(max_digits=16, decimal_places=8)
	value = models.DecimalField(max_digits=16, decimal_places=8)

	def update_value(self):
		response = auth_client.get_account(self.cb_id)
		self.quantity = float(response['balance'])
		self.available = float(response['available'])
		self.hold = float(response['hold'])
		if self.currency == 'USD':
			self.price = 1
		else:
			response = auth_client.get_product_ticker(product_id='%s-USD'%(self.currency))
			self.price = float(response['price'])
		self.value = self.quantity * self.price
		self.save()