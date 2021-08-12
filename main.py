import pandas as pd

data = pd.read_csv('./Data/BANKNIFTY.csv')

BUY = False
SELL = False
EARNING = 0
CONDITION = ''
PROFIT = ''
BUY_RATE = 0
THRESHOLD = 0
DECISION_POINT = True
DECISION = 0
VERIFICATION_POINT = False
HIGH = 0
LOW = 0
STOP_LOSS = 0.5 / 100
STOP_LOSS_VAL = 0
EXPIRY = True
TRADE_TIME = '09:30'
TRADE_END = '15:30'

for i in range(len(data)):
    date, time, opening, high, low, closing = data['Date'][i], data['Time'][i], data['Open'][i], data['High'][i], data['Low'][i], data['Close'][i]

    if DECISION_POINT:
        if high > HIGH or HIGH == 0:
            HIGH = high
        if low < LOW or LOW == 0:
            LOW = low

        if EXPIRY:
            THRESHOLD = opening
            EXPIRY = False
        DECISION = closing

        if TRADE_TIME == time:
            if DECISION >= THRESHOLD:
                BUY = True
                CONDITION = 'BUY'
                STOP_LOSS_VAL = DECISION - (DECISION * STOP_LOSS)
            elif DECISION < THRESHOLD:
                SELL = True
                CONDITION = 'SELL'
                STOP_LOSS_VAL = DECISION + (DECISION * STOP_LOSS)
            EXPIRY = True
            DECISION_POINT = False
            VERIFICATION_POINT = True

    if VERIFICATION_POINT:
        if TRADE_TIME == time:
            print('HIGH: {}, LOW: {}, STOP LOSS: {}, CONDITION: {}'.format(HIGH, LOW, STOP_LOSS_VAL, CONDITION))

        if BUY and STOP_LOSS_VAL >= closing:
            TRADE_END = '15:15'

        if SELL and STOP_LOSS_VAL <= closing:
            TRADE_END = '15:15'

        if TRADE_END == time:
            if BUY:
                EARNING = closing - DECISION
            if SELL:
                EARNING = DECISION - closing

            if EARNING > 0:
                PROFIT = "PROFIT"
            else:
                PROFIT = "LOSS"

            PROFIT_PERCENT = EARNING * 100 / DECISION
            if PROFIT_PERCENT < 0:
                PROFIT_PERCENT *= -1

            print(f'{date} {time} ---> DECISION: {CONDITION} AT: {DECISION} Closing: {closing} WITH {PROFIT} OF {PROFIT_PERCENT}\n')
            DECISION_POINT = True
            VERIFICATION_POINT = False
            BUY = SELL = False
            HIGH = LOW = 0
            EARNING = 0
            CONDITION = ''
            DECISION = 0
            PROFIT = ''
            TRADE_END = '15:30'


