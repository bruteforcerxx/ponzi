from .models import Transaction
from users.models import User
from threading import Thread
from decimal import Decimal
import time
import requests
import json
from .funding_manager_luno import funding_manager_luno 
import string
import random
from rest_framework.response import Response
from rest_framework import status

in_use_l = False


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def send_to_luno(user_id, amount, address, desc, x):
    global in_use_l
    print(x)
    if x < 5:
        try:
            user = User.objects.get(id=user_id)
            file_a = open('jsons/luno_funded_keys.json', 'r')
            keys = json.load(file_a)
            file_a.close()
            key = keys[0]
            secret_key = key[0]
            key_id = key[1]
            payload = {'amount': amount, 'currency': 'XBT', 'address': address,
                        'description': 'desc'}
            r = requests.get('https://api.mybitx.com/api/1/send', params=payload)
            print('sending request to luno...')
            response = requests.post(r.url, auth=(key_id, secret_key)).json()
            print(response)

            user.balance = Decimal(user.balance) - Decimal(amount)
            transaction = Transaction()
            transaction.by = user
            transaction.tx_hash = id_generator()
            transaction.amount = Decimal(amount)
            transaction.summary = 'withdrawal'
            transaction.type = 'debit'
            transaction.description = "Withdrawal of %d %s made into %s's (%s) account" % (Decimal(amount), 'BTC', user.username, user.email)
            transaction.status = 'complete'

            user.save()

            transaction.save()
            
            for key in response:
                if key == 'success':
                    #rearrange and save keys
                    used_key = keys[0]
                    keys.remove(keys[0])
                    keys.append(used_key)
                    file_update = open('luno_funded_keys.json', 'w')
                    json.dump(keys, file_update)
                    file_update.close()
                    return 'success'

                elif key == 'error':
                    file_a = open('jsons/luno_awaiting_fund.json', 'r')
                    awaiting_keys = json.load(file_a)
                    file_a.close()
                    awaiting_keys.insert(0, keys[0])

                    file_update = open('jsons/luno_awaiting_fund.json', 'w')
                    json.dump(awaiting_keys, file_update)
                    file_update.close()
                    keys.remove(keys[0])
                    file_update = open('jsons/luno_funded_keys.json', 'w')
                    json.dump(keys, file_update)
                    file_update.close()
                    time.sleep(1)
                    trials = [0]

                    thread_l = Thread(target=funding_manager_luno, args=trials)
                    thread_l.start()

                    print('retrying transaction...')
                    x += 1
                    send_to_luno(user_id, amount, address, desc, x)
                

        except IndexError:
            print('No new keys available in funded list!!')
            print('waiting for keys...\n')
            time.sleep(5)
            print('retrying transaction...')
            x += 1
            send_to_luno(user_id, amount, address, desc, x)

        except Exception as e:
            print(e)    
            x += 1
   

    else:
        print('failed')
        return 'failed'
        
    