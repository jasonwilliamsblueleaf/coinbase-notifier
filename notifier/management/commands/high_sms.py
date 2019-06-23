from django.core.management.base import BaseCommand, CommandError
import os, requests
from cbimporter.models import cb_portfolio

TILL_URL = os.environ.get("TILL_URL")

class Command(BaseCommand):
	def handle(self, *args, **options):
		cb_portfolio.update_all()
		if cb_portfolio.is_high():
			cb_portfolio.update_high()
			sms_text = 'New High!\nTotal Value: $%s'%(round(cb_portfolio.total_value,2))
			for account in cb_portfolio.account_set.all():
				sms_text += '\n%s price: %s'%(account.currency, round(account.price, 2))
			requests.post(TILL_URL, json={
			    "phone": os.environ.get("CELL_PHONE"),
			    "text" : sms_text
			})