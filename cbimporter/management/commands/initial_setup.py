from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cbimporter.models import auth_client, Portfolio, Account

class Command(BaseCommand):
	def handle(self, *args, **options):
		response = auth_client.get_accounts()
		portfolio = Portfolio(total_value = 0, high_date = timezone.now(), high_value = 0)
		portfolio.save()
		for account in response:
			if float(account['balance']) != 0:
				portfolio.account_set.create(
					cb_id = account['id'],
					currency = account['currency'],
					quantity = account['balance'],
					available = account['available'],
					hold = account['hold'],
					price = 0,
					value = 0
					)
		self.stdout.write(self.style.SUCCESS('Setup successful'))