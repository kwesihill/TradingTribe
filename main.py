# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tradingview_ta import TA_Handler, Interval, get_multiple_analysis
from ta import add_all_ta_features
import tradingview_ta, requests, argparse
import pandas as pd
from datetime import *
from decimal import *
import pandas_ta as _ta
import yahoo_fin.stock_info as si
import yfinance as yf
from lightweight_charts import Chart
import datetime as dt
from datetime import *
from decimal import *
from datetime import datetime
from pandas_datareader import data as pdr
from dateutil.relativedelta import relativedelta


def main(name):
    from tradingview_ta import TA_Handler, Interval, Exchange


# _data = add_all_ta_features(si.get_data("aapl"), open="open", high="high", low="low", close="close",ema="ema", volume="volume",MA="MA")


# Press the green button in the gutter to run the script..

slow = Decimal('150.000')  # Slow Moving Average
fast = Decimal('15.000')  # Fast Moving Average
heat = Decimal('0.100')  # Account Heat
skid = Decimal('0.500')  # Entry/Exit Price Skid
comm = Decimal('0.000')  # Commissions
atrm = Decimal('5.000')  # Average True Range Risk Multiplier
atrt = Decimal('20.000')  # Average True Range Lag
risk = Decimal('0.000')  # Per Trade Risk

start_equity = Decimal('1000000.00')  # Starting Account Equity

TWO_PLACES = Decimal('1.00')
THREE_PLACES = Decimal('1.000')

weekdays = {0: 'M', 1: 'T', 2: 'W', 3: 'H', 4: 'F', 5: 'S', 6: 'U'}

def heikinashi(df: pd.DataFrame) -> pd.DataFrame:
    df_HA = df.copy()
    df_HA['Close'] = (df_HA['open'] + df_HA['high'] + df_HA['low'] + df_HA['close']) / 4

    for i in range(0, len(df)):
        if i == 0:
            df_HA['open'][i] = ((df_HA['open'][i] + df_HA['close'][i]) / 2)
        else:
            df_HA['open'][i] = ((df_HA['open'][i - 1] + df_HA['close'][i - 1]) / 2)

    df_HA['high'] = df_HA[['open', 'close', 'high']].max(axis=1)
    df_HA['low'] = df_HA[['open', 'close', 'low']].min(axis=1)
    return df_HA



class Trade:
    def __init__(self, units, entry_price):
        self.units = units
        self.entry = Decimal(entry_price)
        self.exit = Decimal('0.00')
        self.pnl = Decimal('0.00')

    def update(self, price):
        self.pnl = self.units * (Decimal(price) - self.entry)
        return self.pnl

    def __str__(self):
        return "units=%d, pnl=%s, entry=%s, exit=%s" % (self.units,
                                                        self.pnl.quantize(TWO_PLACES),
                                                        self.entry.quantize(TWO_PLACES),
                                                        self.exit.quantize(TWO_PLACES))
class BackOffice:
    def __init__(self, initial_balance):
        self.balance = Decimal(initial_balance)
        self.equity = Decimal('0.00')
        self.open_pnl = Decimal('0.00')
        self.trades = []

    def open_trade(self, t):
        self.trades.append(t)

    def close_trade(self, t):
        self.trades.remove(t)
        self.balance += self.open_pnl

    def update(self, price):
        self.open_pnl = Decimal('0.00')
        for t in self.trades:
            self.open_pnl += t.update(price)
        self.equity = self.balance + self.open_pnl


def round_size(size):
    div = size / 250
    mul = round(div)
    return int(250 * mul)
if __name__ == '__main__':
    yf.pdr_override()
six_yrs_ago = datetime.now() - relativedelta(years=30)
dictTradeData = {}
data = pdr.get_data_yahoo("ES=F", start=six_yrs_ago.strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d'))
data = data.reset_index()
data.columns = data.columns.str.lower()
see = pd.read_csv(r"sp.csv")
print(see)


#print(heikinashi(data.copy()))
bo = BackOffice(start_equity)
2
metrics_log = open('metrics-log.txt', 'w')
trade_log = open('trade-log.txt', 'w')
equity_log = open('equity-log.txt', 'w')

trade_log.write('%6s  %-18s  %-18s  %12s\n' % ('Units', 'Entry', 'Exit', 'P&L'))
trade_log.write('%s  %s  %s  %s\n' % ('-' * 6, '-' * 18, '-' * 18, '-' * 12))

equity_log.write('%8s  %12s  %12s  %12s\n' % ('Date', 'Clo Balance', 'Open Profit', 'Equity'))
equity_log.write('%s  %s  %s  %s\n' % ('-' * 8, '-' * 12, '-' * 12, '-' * 12))

ELf = None  # Fast Exponential Lag
ELs = None  # Slow Exponential Lag
ATR = None  # Average True Range
TCa = (atrt + 1) / 2  # Time constant for ATR
TCf = (fast + 1) / 2  # Time constant for fast MA
TCs = (slow + 1) / 2  # Time constant for slow MA
CLa = Decimal('0.00')  # Yesterday's close
cro = ''

MA_INIT = 0
MA_FOS = 1
MA_SOF = 2

state = MA_INIT

OUT = 0
LONG = 1

mkt_state = OUT

NONE = 0
BUY = 1
SELL = 2

order_state = NONE

warm = True
warm_cycles = 20

i = 0

size = 0
entry_price = Decimal('0.000')
exit_price = Decimal('0.000')

t = None
print(heikinashi(data.copy()))
#_updatedData = heikinashi(data.copy())
_updatedData = pd.read_csv(r"sp.csv")
print(_updatedData)
for index,r in _updatedData.iterrows():
    if i > warm_cycles: warm = False
    i += 1
#date         open     high  ...  adj close   volume      Close
  #date = datetime.strptime(p["date"], "%Y%m%d")


    #print(datetime.strptime(r["date"], "%Y%m%d"))
    #print(r["open"])
    _date = str(r[0])
    print(_date)
    _dateMonth = str(_date[4:6])
    print(_dateMonth)
    _datey = str(_date[:4])
    print(_datey)
    _dateDay = str(_date[6:8])
    print(_dateDay)
    #data["Name"] = data["Name"].str.cat(_date[4:6), sep="-").str.cat(str(r[0][:-2]), sep="-")
    date = _dateMonth + '-' +_dateDay  + '-' +_datey
    print(date)
    op = Decimal(r[1])
    hi = Decimal(r[2])
    lo = Decimal(r[3])
    cl = Decimal(r[4])
    #date = pd.to_datetime(str(_date), format='%Y-%m-%d', errors='ignore')
    #date = datetime.datetime.strptime(_date, '%Y%m%d')
    if order_state == BUY:
        mkt_state = LONG
        order_state = NONE
        entry_price = op + skid * (hi - op)
        t = Trade(size, entry_price)
        bo.open_trade(t)
        trade_log.write('%6s  %s %9s  ' %
                    (size, date,
                     entry_price.quantize(THREE_PLACES)))

    elif order_state == SELL:
        mkt_state = OUT
        order_state = NONE
        exit_price = op - skid * (op - lo)
        pnl = size * (exit_price - entry_price)
        bo.close_trade(t)
        trade_log.write('%s %9s  %12s\n' %
                    (date,
                     exit_price.quantize(THREE_PLACES),
                     pnl.quantize(TWO_PLACES)))

    bo.update(cl)

    equity_log.write('%8s  %12s  %12s  %12s\n' %
                     (date,
                      bo.balance.quantize(TWO_PLACES),
                      bo.open_pnl.quantize(TWO_PLACES),
                      bo.equity.quantize(TWO_PLACES)))

    if ELf == None: ELf = cl
    if ELs == None: ELs = cl
    if ATR == None:
        tr = hi - lo
        ATR = tr
    else:
        tr = max(hi, CLa) - min(lo, CLa)

    CLa = cl

    ELf = Decimal(ELf + 1 * (cl - ELf) / TCf)
    ELs = Decimal(ELs + 1 * (cl - ELs) / TCs)
    ATR = Decimal(ATR + 1 * (tr - ATR) / TCa)

    if ELf > ELs:
        # buy signal
        if warm == False and state == MA_SOF:
            order_state = BUY
            risk = atrm * ATR
            size = round_size((bo.equity * heat) / risk)
        state = MA_FOS
        cro = ' +'

    elif ELf < ELs:
        # sell signal
        if warm == False and state == MA_FOS and mkt_state == LONG:
            order_state = SELL
        state = MA_SOF
        cro = ' -'
print(date)
metrics_log.write('%s-%s Eq=%s  OHLC:[ %s %s %s %s ] slow=%s fast=%s Atr=%s%s\n' %
                      (date, date,
                       bo.equity.quantize(TWO_PLACES),
                       op.quantize(TWO_PLACES),
                       hi.quantize(TWO_PLACES),
                       lo.quantize(TWO_PLACES),
                       cl.quantize(TWO_PLACES),
                       ELs.quantize(THREE_PLACES),
                       ELf.quantize(THREE_PLACES),
                       ATR.quantize(THREE_PLACES),
                       cro))



