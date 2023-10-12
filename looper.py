
import stablecoin_bot
import random_bot
import time 

LOOP_WAIT_MINUTES=10

if __name__ == "__main__":
    while True:
        stablecoin_bot.main_loop()
        random_bot.main_loop()
        print(f"Waiting for {LOOP_WAIT_MINUTES} minutes...")
        time.sleep(60*LOOP_WAIT_MINUTES)