from tiramisu_wallet_client import TiramisuClient
import random
import time 

LOOP_WAIT_MINUTES = 30
ONE_SALE_PERCENTAGE = 0.01
ONE_SALE_MAX = 500

USERNAME_BTC_ACCOUNT = 'XXX'
PASSWORD_BTC_ACCOUNT = 'YYY'

client_btc_account = TiramisuClient(username=USERNAME_BTC_ACCOUNT,password=PASSWORD_BTC_ACCOUNT)

def main_loop():

    listings = client_btc_account.listings()
    balances = client_btc_account.balances()
    num_assets_to_sell = random.randint(1, 20)
    balances = [bal for bal in balances if bal['balance']>0]
    random.shuffle(balances)
    balances_selected_for_sale = balances[0:num_assets_to_sell]

    for balance in balances_selected_for_sale:
        
        currency_id = balance['currency']
        currency = client_btc_account.asset(id=currency_id)
        
        if currency['name']=='Bitcoin':
            print('BTC currency, Continuing...')
            continue 
         
        balance = balance['balance']
        if balance==0:
            print('zero balance, Continuing...')
            continue 
        

        amount_sell = int(int(random.randint(0, 5))*balance/5)
        
        if amount_sell==0:
            amount_sell = 1
        
        print(f"Selling {amount_sell} worth of currency {currency_id} ...")
        try:
            client_btc_account.sell_taproot_asset(asset=currency_id, amount=amount_sell)
        except Exception as e:
            s = str(e)
            if "Please enter an amount larger than " in s and len(s)<2000:
                print(s)
                amount_sell = int(s.split(" and smaller than ")[1].split(" ")[0])
                try:
                    print(f"Selling {amount_sell} worth of currency {currency_id} ...")
                    client_btc_account.sell_taproot_asset(asset=currency_id, amount=amount_sell)
                except Exception as e:
                    s = str(e)
                    print(s)
                    
        print("done.")

    btc_balance = client_btc_account.get_btc_balance()["balance"]

    num_assets_to_buy = random.randint(1, 20)
    random.shuffle(listings)
    listings_selected_for_sale = listings[0:num_assets_to_buy]
    for listing in listings_selected_for_sale:
        
        currency_id = listing['currency']
        price_sat = listing['price_sat']
        currency = client_btc_account.asset(id=currency_id)
        supply = currency['supply']

        amount_buy = int(10**random.randint(0, 5))
        print(f"Buying {amount_buy} worth of currency {currency_id} ...")
        try:
            client_btc_account.buy_taproot_asset_asset(asset=currency_id, amount=amount_buy)
        except Exception as e:
            
            s = str(e)
            print(s)
            
        print("done.")

if __name__ == "__main__":
    while True:
        main_loop()
        print(f"Waiting for {LOOP_WAIT_MINUTES} minutes...")
        time.sleep(60*LOOP_WAIT_MINUTES)