

from tiramisu_wallet_client import TiramisuClient
import yfinance as yf
import time 

LOOP_WAIT_MINUTES = 10

LISTING_ID=11
currency_id = 131
USERNAME_USD_ACCOUNT = 'XXX'
USERNAME_BTC_ACCOUNT = 'YYY'
PASSWORD_BTC_ACCOUNT = 'ZZZ'

client_btc_account = TiramisuClient(username=USERNAME_BTC_ACCOUNT,password=PASSWORD_BTC_ACCOUNT)
client_usd_account = TiramisuClient(username=USERNAME_USD_ACCOUNT,password=PASSWORD_BTC_ACCOUNT)

usd_user_id = client_usd_account.get_btc_balance()['user']
btc_user_id = client_btc_account.get_btc_balance()['user']

def main_loop():

    # listing = client_btc_account.listing(id=LISTING_ID)
    
    # price_sat = listing["price_sat"]
    # currency_id = listing["currency"]
    
    balances = client_usd_account.balances()
    
    coin_balance = [b for b in balances if b['currency']==currency_id][0]['balance']
    btc_balance = client_usd_account.get_btc_balance()["balance"]

    ticker_yahoo = yf.Ticker("BTC-USD")
    data = ticker_yahoo.history()
    last_quote = data['Close'].iloc[-1]
    print("BTC-USD", last_quote)
    
    price_to_be =1/last_quote*10000000/10000
    
    print("price_to_be")
    print(price_to_be)
    
    btc_balance_future = price_to_be*coin_balance
    
    diff = int(btc_balance_future - btc_balance)
    
    print(diff)
    
    if diff > 0:
        print(diff)
        client_btc_account.transactions_send_internal(destination_user=usd_user_id,asset=1,amount=diff,description="Stablecoin price adjustment.")
    
    if diff < 0:
        print(diff)
        client_usd_account.transactions_send_internal(destination_user=btc_user_id,asset=1,amount=-diff,description="Stablecoin price adjustment.")
    
    
    
if __name__ == "__main__":
    while True:
        main_loop()
        print(f"Waiting for {LOOP_WAIT_MINUTES} minutes...")
        time.sleep(60*LOOP_WAIT_MINUTES)