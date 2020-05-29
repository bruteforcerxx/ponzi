import requests
import time
import json
from coinbase.wallet.client import Client

def funding_manager_luno(trial):
    print('\n############LUNO FUNDING##############')

    if trial < 5:
        try:
            file_a = open('jsons/luno_awaiting_fund.json', 'r')
            a_f = json.load(file_a)
            file_a.close()

            x = a_f[0]

            a = time.time()
            print(f'luno non_funded keys detected\n')
            print(f'trial {trial}\n')

            file_update = open('jsons/luno_funded_keys.json', 'r')
            funded = json.load(file_update)
            file_update.close()

            print(f'checking balance of non_funded luno key: {x}...\n')

            payload = {'asset': 'XBT'}
            r = requests.get('https://api.mybitx.com/api/1/balance', params=payload)
            rs = requests.get(r.url, auth=(x[1], x[0])).json()
            old_bal = rs['balance'][0]['balance']

            print(f'balance of {x} = {old_bal}\n')

            balance_sheet_w_id = []
            balance_list = []

            print(f'checking balance of luno funded keys...')

            if len(funded) > 0:
                for i in funded:
                    payload = {'asset': 'XBT'}
                    r = requests.get('https://api.mybitx.com/api/1/balance', params=payload)
                    rs = requests.get(r.url, auth=(i[1], i[0])).json()
                    balance = float(rs['balance'][0]['balance'])
                    time.sleep(10)
                    balance_sheet_w_id.append([i[0], i[1], balance])
                    balance_list.append(balance)
                    print(f'balance of {i} = {balance}')

                max_bal = max(balance_list)
                print(f'\nmax balance = {max_bal}\n')
                index = balance_list.index(max_bal)
                use_key = balance_sheet_w_id[index]
                print(f'using key: {use_key}...\n')
            else:
                print('\n!!!!!no funded keys available!!!!!\n')
                use_key = [0.000, 0.000, 0.000]

            print(f'{float(use_key[2])}    {float(old_bal)} \n')

            if float(use_key[2]) > float(old_bal):
                print('trying to initiate re-funding with luno...\n')

                try:
                    amount_rf = float(use_key[2]) / 2
                    amount_rf = f"{amount_rf:.8f}"
                    amt_rf = str(amount_rf)
                    print(f'sending {amt_rf} to {x[2]}...\n')

                    payload = {'amount': amt_rf, 'currency': 'XBT', 'address': x[2],
                               'description': 're-fundinng process'}
                    print(f'Transferring {amount_rf} to account: {x[2]}')
                    s = requests.get('https://api.mybitx.com/api/1/send', params=payload)
                    r_f = requests.post(s.url, auth=(use_key[1], use_key[0])).json()
                    print(r_f)

                    suc = []
                    for k, v in r_f.items():
                        suc.append(k)
                        suc.append(v)
                    if 'success' in suc:
                        file_a = open('jsons/luno_awaiting_fund.json', 'r')
                        awaiting_keys_2 = json.load(file_a)
                        file_a.close()

                        awaiting_keys_2.remove(x)

                        file_remove = open('jsons/luno_awaiting_fund.json', 'w')
                        json.dump(awaiting_keys_2, file_remove)
                        file_remove.close()

                        file_update = open('jsons/luno_funded_keys.json', 'r')
                        funded = json.load(file_update)
                        file_update.close()

                        funded.append(x)

                        file_update = open('jsons/luno_funded_keys.json', 'w')
                        json.dump(funded, file_update)
                        file_update.close()
                        time.sleep(1)

                        b = time.time()
                        print(f'luno funded keys transfer time: {b - a}\n\n')
                    else:
                        funding_manager_luno(trial + 1)

                except Exception as e:
                    print(e)
                    funding_manager_luno(trial + 1)

            else:
                print('insufficient funds in all luno keys\n')
                print('retrying re-funding with coinbase...\n')
                print(f'getting address of {x}...\n')

                payload = {'asset': 'XBT'}
                r = requests.get('https://api.mybitx.com/api/1/funding_address', params=payload)
                rs = requests.get(r.url, auth=(x[1], x[0])).json()
                btc_address = rs['address']

                print(f'btc address of {x}:  {btc_address}\n')

                cb_funded = open('jsons/coinbase_funded_keys.json', 'r')
                funded = json.load(cb_funded)
                cb_funded.close()

                cb_balance_sheet_w_id = []
                balance_lst = []

                print('checking balance in all coinbase accounts...')
                for a in funded:
                    print(f'checking {a}...')
                    client_a = Client(a[1], a[0])
                    account = client_a.get_account('BTC')
                    bal = float(account['balance']['amount'])
                    cb_balance_sheet_w_id.append([a[0], a[1], a[2], bal])
                    balance_lst.append(bal)
                    print(f'balance of {a}: {bal}\n')

                cb_max_bal = max(balance_lst)
                ind = balance_lst.index(cb_max_bal)
                use_key = cb_balance_sheet_w_id[ind]

                print(f'balance list: {balance_lst}')
                print(f'max balance in all coinbase accounts = {cb_max_bal}\n')

                try:
                    print('trying to initiate re-funding with coinbase...\n')

                    amount = cb_max_bal / 2
                    amount = f"{amount:.8f}"
                    print(f'btc address of {x} = {btc_address}')

                    client_b = Client(use_key[1], use_key[0])
                    tx = client_b.send_money(use_key[2], to=btc_address, amount=amount, currency='BTC')
                    print(tx)

                    suc = []
                    for k, v in tx.items():
                        suc.append(k)
                        suc.append(v)

                    if 'completed' in suc:
                        file_a = open('jsons/coinbase_awaiting_fund.json', 'r')
                        awaiting_keys_2 = json.load(file_a)
                        file_a.close()

                        awaiting_keys_2.remove(x)

                        file_remove = open('jsons/coinbase_awaiting_fund.json', 'w')
                        json.dump(awaiting_keys_2, file_remove)
                        file_remove.close()

                        w = old_bal

                        while w == old_bal:
                            payload = {'asset': 'XBT'}
                            r = requests.get('https://api.mybitx.com/api/1/balance', params=payload)
                            rs = requests.get(r.url, auth=(x[1], x[0])).json()
                            w = float(rs['balance'][0]['balance'])
                            time.sleep(900)

                        file_update = open('jsons/luno_funded_keys.json', 'r')
                        funded = json.load(file_update)
                        file_update.close()

                        funded.append(x)

                        file_update = open('jsons/luno_funded_keys.json', 'w')
                        json.dump(funded, file_update)
                        file_update.close()
                        time.sleep(1)

                        b = time.time()
                        print(f'luno funded keys transfer time: {b - a}\n\n')
                    else:
                        funding_manager_luno(trial + 1)

                except Exception as e:
                    print(e)
                    time.sleep(5)
                    funding_manager_luno(trial + 1)

        except Exception as e:
            print(e)
            time.sleep(5)
            funding_manager_luno(trial + 1)

    else:
        print('maximum trials exceeded')