import os
from dotenv import load_dotenv
load_dotenv()
from threading import Timer
from transactions.models import Transaction
import requests
import time
from decimal import Decimal 
from coinbase.wallet.client import Client

def balanceLuno():
  pending_luno_txs = Transaction.objects.filter(service='luno', status='pending', type='debit', summary='withdrawal')
  total_amount = 0
  if len(pending_luno_txs) > 0:
    for p in pending_luno_txs:
      total_amount += p.amount
    payload = {'asset': 'XBT'}
    r = requests.get('https://api.mybitx.com/api/1/balance', params=payload)
    rs = requests.get(r.url, auth=(os.environ['LUNO_KEY_ID'], os.environ['LUNO_SECRET_KEY'])).json()
    luno_total_balance = rs['balance'][0]['balance']
    luno_reserve_balance = rs['balance'][0]['reserved']
    luno_balance = Decimal(luno_total_balance) - Decimal(luno_reserve_balance)
    print('luno balance', luno_balance)
    if Decimal(luno_balance) < total_amount:
      r = requests.get('https://api.mybitx.com/api/1/funding_address', params=payload)
      rs = requests.get(r.url, auth=(os.environ['LUNO_KEY_ID'], os.environ['LUNO_SECRET_KEY'])).json()
      luno_address = rs['address']

      #you will insert a code to call the @api view function for sending to coinbase here#
      
      client = Client(os.environ['COINBASE_API_KEY'], os.environ['COINBASE_API_SERCRET'], api_version='YYYY-MM-DD')
      primary_account = client.get_primary_account()
      try:
        tx = primary_account.send_money(to=luno_address, amount=float(total_amount), currency='BTC')
      except Exception as e:
        print(str(e))
      luno_balance = Decimal(luno_balance)
      while luno_balance < total_amount:
        time.sleep(3) #15 minutes
        payload = {'asset': 'XBT'}
        r = requests.get('https://api.mybitx.com/api/1/balance', params=payload)
        rs = requests.get(r.url, auth=(os.environ['LUNO_KEY_ID'], os.environ['LUNO_SECRET_KEY'])).json()
        print(rs)
        luno_total_balance = rs['balance'][0]['balance']
        luno_reserve_balance = rs['balance'][0]['reserved']
        luno_balance = Decimal(luno_total_balance) - Decimal(luno_reserve_balance)
        print(luno_balance)
    else:  
      pass

    #make payments
    for p in pending_luno_txs:
      payload = {'amount': p.amount, 'currency': 'XBT', 'address': p.to, 'description': 'descripton'}
      r = requests.get('https://api.mybitx.com/api/1/send', params=payload)
      print('sending request to luno...')
      print(p.tx_hash)
      rs = requests.post(r.url, auth=(os.environ['LUNO_KEY_ID'], os.environ['LUNO_SECRET_KEY'])).json()
      print(rs)
      if 'success' in rs:
        p.status = 'complete'
        p.save()
      else:
        pass
  else:
    pass
