from binance.client import Client
import time
import os

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
c = Client(API_KEY, API_SECRET)
SYM = "XRPUSDT"
last = None
print("BOT START - SERVER PE CHAL RAHA HAI")

while True:
    try:
        p = float(c.futures_symbol_ticker(symbol=SYM)['price'])
        print("Price:", p, flush=True)
        pos = c.futures_position_information(symbol=SYM)
        amt = 0
        entry = 0
        for x in pos:
            if float(x['positionAmt']) != 0:
                amt = float(x['positionAmt'])
                entry = float(x['entryPrice'])
        if amt == 0:
            if last is not None:
                qty = 5 / p
                if qty < 1:
                    qty = 1
                if p > last:
                    c.futures_create_order(symbol=SYM, side='BUY', type='MARKET', quantity=round(qty,1))
                    print("BUY Ho Gaya", flush=True)
                if p < last:
                    c.futures_create_order(symbol=SYM, side='SELL', type='MARKET', quantity=round(qty,1))
                    print("SELL Ho Gaya", flush=True)
        else:
            if amt > 0:
                pnl = (p - entry) / entry * 100
            else:
                pnl = (entry - p) / entry * 100
            print("PnL:", pnl, flush=True)
            if pnl <= -5 or pnl >= 5:
                side = 'SELL' if amt > 0 else 'BUY'
                c.futures_create_order(symbol=SYM, side=side, type='MARKET', quantity=abs(amt))
                print("Pos Band", flush=True)
        last = p
        time.sleep(60)
    except Exception as e:
        print("Err:", e, flush=True)
        time.sleep(10)
