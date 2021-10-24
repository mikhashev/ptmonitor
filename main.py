from openapi_client import openapi

import datetime
from time import sleep
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


def get_token():
    with open('my_ti_token.txt', "r") as file:
        token = file.read()

    return token


# connect to api
client = openapi.api_client(get_token())


def get_stocks_to_list():
    """
    function get two stock lists,
    one that trades in RUB currency, second in USD currency

    example of raw data from api:
        {'currency': 'USD',
      'figi': 'BBG001WTBC36',
      'isin': 'US7374461041',
      'lot': 1,
      'min_price_increment': 0.01,
      'name': 'Post Holdings Inc',
      'ticker': 'POST',
      'type': 'Stock'},

    :return: tuple(list[], list[])
    """

    stocks = client.market.market_stocks_get()

    instr_list = stocks.payload.instruments

    rub_stocks = []
    usd_stocks = []
    for stock in instr_list:
        ticker_name = stock.ticker
        ticker_currency = stock.currency
        print(stock)

        # classification by currency
        if ticker_currency == 'RUB':
            rub_stocks.append(ticker_name)

        elif ticker_currency == 'USD':
            usd_stocks.append(ticker_name)

    print('stocks trade in RUB currency: ', len(rub_stocks))
    print(rub_stocks)
    print('stocks trade in USD currency: ', len(usd_stocks))
    print(usd_stocks)

    return rub_stocks, usd_stocks


def get_all_stocks_list():
    stocks = client.market.market_stocks_get()
    instruments = stocks.payload.instruments
    return instruments


def rub_stocks_from_list(stocks) -> list:
    rub_stocks = []

    for stock in stocks:
        ticker_currency = stock.currency

        if ticker_currency == 'RUB':
            rub_stocks.append(stock)

    return rub_stocks


def get_figi_by_ticker(ticker) -> str:
    ticker_data = client.market.market_search_by_ticker_get(ticker)  # get ticker by figi

    figi_data = ticker_data.payload.instruments[0]
    figi = figi_data.figi
    return figi


def get_orderbook(ticker=str("VTBR"), depth=int(900)):
    orderbook_data = client.market.market_orderbook_get_with_http_info(get_figi_by_ticker(ticker), depth)

    orderbook_data = orderbook_data[0]
    orderbook_data = (orderbook_data.payload)

    asks_price_total = float()
    asks_quantity_total = int()
    bids_price_total = float()
    bids_quantity_total = int()

    # print("Asks:", len(orderbook_data.asks))
    # print(orderbook_data.asks)

    asks_price_60 = float()
    asks_quantity_60 = int()
    bids_price_60 = float()
    bids_quantity_60 = int()

    asks_price_more_60 = float()
    asks_quantity_more_60 = int()
    bids_price_more_60 = float()
    bids_quantity_more_60 = int()

    # todo use lots size  to calculate price?

    count_asks = 0
    for ask_bid in orderbook_data.asks:

        asks_quantity_total += ask_bid.quantity
        asks_price_total += ask_bid.price * float(ask_bid.quantity)
        count_asks += 1
        if count_asks <= 59:
            asks_quantity_60 += ask_bid.quantity
            asks_price_60 += ask_bid.price * float(ask_bid.quantity)
        elif count_asks >= 59:
            asks_quantity_more_60 += ask_bid.quantity
            asks_price_more_60 += ask_bid.price * float(ask_bid.quantity)

    # print("Bids:", len(orderbook_data.bids))
    # print(orderbook_data.bids)
    count_bids = 0

    for bid in orderbook_data.bids:

        bids_quantity_total += bid.quantity
        bids_price_total += bid.price * float(bid.quantity)
        count_bids += 1
        if count_bids <= 59:
            bids_quantity_60 += bid.quantity
            bids_price_60 += bid.price * float(bid.quantity)
        elif count_bids >= 59:
            bids_quantity_more_60 += bid.quantity
            bids_price_more_60 += bid.price * float(bid.quantity)

    # 'close_price': 15313.0,
    # 'depth': 900,
    # 'face_value': None,
    # 'figi': 'BBG000R607Y3',
    # 'last_price': 15790.5,
    # 'limit_down': 14234.5,
    # 'limit_up': 16418.5,
    # 'min_price_increment': 0.5,

    # 'trade_status': 'NormalTrading'}

    # break_in_trading - торги приостановлены;
    # normal_trading - торги идут;
    # not_available_for_trading - торги не идут;
    # closing_auction - торги в аукционе закрытия;
    # closing_period - торги в периоде закрытия;
    # discrete_auction - торги в дискретном аукционе;
    # opening_period - торги в аукционе открытия;
    # trading_at_closing_auction_price - торги по цене аукциона закрытия

    # print(orderbook_data)

    # print('\nclose_price: ', orderbook_data.close_price)
    # print('last_price: ', orderbook_data.last_price)
    # print('limit_up: ', orderbook_data.limit_up)
    # print('limit_down: ', orderbook_data.limit_down)
    # print('min_price_increment: ', orderbook_data.min_price_increment)
    #
    # print("trade_status:", orderbook_data.trade_status)
    #
    # print("\nasks_price_total:", asks_price_total)
    # print("asks_quantity_total:", asks_quantity_total)
    # print("bids_price_total:", bids_price_total)
    # print("bids_quantity_total:", bids_quantity_total)
    # asks_bids_ratio = round(asks_quantity_total/bids_quantity_total, 3)
    aks_bids_price_ratio = round(asks_price_total / bids_price_total, 3)
    # print("Ask/Bids price ratio: ", aks_bids_price_ratio)
    # print("Ask/Bids quantity ratio: ", asks_bids_ratio)
    # asks_bids_60_ratio = round(asks_quantity_60/bids_quantity_60, 3)
    # aks_bids_price_60_ratio = round(asks_price_60/bids_price_60, 3)
    # print("Ask/Bids <60 price ratio: ", asks_bids_60_ratio)
    # print("Ask/Bids <60 quantity ratio: ", aks_bids_price_60_ratio)
    #
    # asks_bids_more_60_ratio = round(asks_quantity_more_60/bids_quantity_more_60, 3)
    # aks_bids_price_more_60_ratio = round(asks_price_more_60/bids_price_more_60, 3)
    # print("Ask/Bids > 60 price ratio: ", asks_bids_more_60_ratio)
    # print("Ask/Bids > 60 quantity ratio: ", aks_bids_price_more_60_ratio)

    # if 1.1 >= aks_bids_price_ratio >= 1:
    #     os.system("say ratio 1")
    #     sleep(1)
    # elif 2.1 >= aks_bids_price_ratio >= 2:
    #     #os.system("say ratio 2")
    # if 0.5 >= aks_bids_price_ratio >= 0:
    #     os.system("say ratio 0.5")
    #     sleep(1)

    return aks_bids_price_ratio


def find_ticker_price_by(figi):
    now = datetime.datetime.utcnow()
    created_at = now - datetime.timedelta(days=3)
    current_time = now.isoformat("T", timespec="seconds") + "Z"
    minute_before = created_at.isoformat("T", timespec="seconds") + "Z"

    interval = "day"

    candles_data = (
        client.market.market_candles_get(figi=figi, _from=minute_before, to=current_time, interval=interval))

    return candles_data


def get_ticker_price(ticker):
    """
    This function get data from api and return ticker price
    return current price of the ticker

    {'c': 288.21,
     'figi': 'BBG004730N88',
     'h': 288.21,
     'interval': '1min',
     'l': 288.12,
     'o': 288.18,
     'time': datetime.datetime(2021, 4, 21, 14, 40, tzinfo=tzutc()),
     'v': 3040}
    """

    figi = get_figi_by_ticker(ticker)

    now = datetime.datetime.utcnow()
    created_at = now - datetime.timedelta(days=1)
    current_time = now.isoformat("T", timespec="seconds") + "Z"
    minute_before = created_at.isoformat("T", timespec="seconds") + "Z"

    interval = "day"

    candles_data = (
        client.market.market_candles_get(figi=figi, _from=minute_before, to=current_time, interval=interval))

    # print(candles_data)
    # need to get last minute close ticker price
    #
    # if len(candles_data.payload.candles) != 0:
    #     average_price = [True, round((candles_data.payload.candles[0].h + candles_data.payload.candles[0].l) / 2, 3)]
    #
    #     return average_price
    # else:
    #     return [False, 0]


# print(client.market.market_stocks_get())

# print(client.market.market_search_by_ticker_get("BANE"))
# print(type(get_stocks_to_list()))
# get_orderbook("MAIL", 10)
# get_ticker_price("MAIL")


def update_orderbook():
    count = 0
    t1_min = 0
    t2_min = 0
    t5_min = 0
    t15_min = 0
    t30_min = 0
    t60_min = 0
    t4_h = 0

    t1_aks_bids_price_ratio = []
    t2_aks_bids_price_ratio = []
    t5_aks_bids_price_ratio = []
    t15_aks_bids_price_ratio = []
    t30_aks_bids_price_ratio = []
    t60_aks_bids_price_ratio = []
    t4h_aks_bids_price_ratio = []

    t1_average_ask_bid = 0
    t2_average_ask_bid = 0
    t5_average_ask_bid = 0
    t15_average_ask_bid = 0
    t30_average_ask_bid = 0
    t60_average_ask_bid = 0
    t4h_average_ask_bid = 0

    while True:

        sleep(1)  # for /market 240 requests/ per 1 minute
        ask_bid_1_sec = get_orderbook("ALRS", 2000)
        t1_aks_bids_price_ratio.append(float(ask_bid_1_sec))
        t1_min += 1
        t2_min += 1
        t5_min += 1
        t15_min += 1
        t30_min += 1
        t60_min += 1
        t4_h += 1

        count += 1

        if t1_min == 59:
            t1_average_ask_bid = sum(t1_aks_bids_price_ratio) / len(t1_aks_bids_price_ratio)

            t2_aks_bids_price_ratio.append(float(t1_average_ask_bid))
            t5_aks_bids_price_ratio.append(float(t1_average_ask_bid))
            t15_aks_bids_price_ratio.append(float(t1_average_ask_bid))
            t30_aks_bids_price_ratio.append(float(t1_average_ask_bid))
            t60_aks_bids_price_ratio.append(float(t1_average_ask_bid))
            t4h_aks_bids_price_ratio.append(float(t1_average_ask_bid))
            t1_min = 0
            t1_aks_bids_price_ratio = []
            print("t1_min_avg:", round(t1_average_ask_bid, 3))
        elif t2_min == 119:
            t2_average_ask_bid = sum(t2_aks_bids_price_ratio) / len(t2_aks_bids_price_ratio)
            t2_min = 0
            t2_aks_bids_price_ratio = []
            print("t2_min_avg:", round(t2_average_ask_bid, 3))

        elif t5_min == 299:
            t5_average_ask_bid = sum(t5_aks_bids_price_ratio) / len(t5_aks_bids_price_ratio)
            t5_min = 0
            t5_aks_bids_price_ratio = []
            print("t5_min_avg:", round(t5_average_ask_bid, 3))

        elif t15_min == 899:
            t15_average_ask_bid = sum(t15_aks_bids_price_ratio) / len(t15_aks_bids_price_ratio)
            t15_min = 0
            t15_aks_bids_price_ratio = []
            print("t15_min_avg:", round(t15_average_ask_bid, 3))
        elif t30_min == 1799:
            t30_average_ask_bid = sum(t30_aks_bids_price_ratio) / len(t30_aks_bids_price_ratio)
            t30_min = 0
            t30_aks_bids_price_ratio = []
            print("t30_min_avg:", round(t30_average_ask_bid, 3))
        elif t60_min >= 3560:
            t60_average_ask_bid = sum(t60_aks_bids_price_ratio) / len(t60_aks_bids_price_ratio)
            t60_min = 0
            t60_aks_bids_price_ratio = []
            print("t60_min_avg:", round(t60_average_ask_bid, 3))

        elif t4_h >= 14400:
            t4h_average_ask_bid = sum(t4h_aks_bids_price_ratio) / len(t4h_aks_bids_price_ratio)
            t4_h = 0
            t4h_aks_bids_price_ratio = []
            print("t4_h_avg:", round(t4h_average_ask_bid, 3))

        print("Count: ", count)
        print("1_sec:", ask_bid_1_sec)
        print("t1_min_avg:", round(t1_average_ask_bid, 3))

        print("t2_min_avg:", round(t2_average_ask_bid, 3))
        print("t5_min_avg:", round(t5_average_ask_bid, 3))
        print("t15_min_avg:", round(t15_average_ask_bid, 3))
        print("t30_min_avg:", round(t30_average_ask_bid, 3))
        print("t60_min_avg:", round(t60_average_ask_bid, 3))
        print("t4h_avg:", round(t4h_average_ask_bid, 3))


def get_prices_for_stocks(list_of_stocks):
    stocks_with_prices = []

    for i in list_of_stocks:
        stock = {}
        # print(i.ticker)
        candles = find_ticker_price_by(str(i.figi))
        price_data = candles.payload.candles

        if len(price_data) != 0:
            one_lot_price = (price_data.pop().c) * (i.lot)

            stock.update({'figi': i.figi,
                          'ticker': i.ticker,
                          'price': one_lot_price})

            stocks_with_prices.append(stock)

    return stocks_with_prices


# update_orderbook()
# stocks_all = get_all_stocks_list()
#
# rub_stocks = rub_stocks_from_list(stocks_all)
#
# ticker_and_prices = (get_prices_for_stocks(rub_stocks))
# list_tickers_and_prices = {}
# for i in ticker_and_prices:
#     ticker_price = {i["ticker"]: i["price"]}
#     list_tickers_and_prices.update(ticker_price)
#
# print(list_tickers_and_prices)
data = {'MDMG': 832.8, 'FIXP': 611.2, 'MOEX': 1710.0, 'MRKU': 1836.0000000000002, 'MRKZ': 588.0, 'TGKB': 4685.0,
        'KZOS': 1024.0, 'YNDX': 5325.8, 'VTBR': 544.0, 'ENPG': 936.5, 'CHMK': 5625.0, 'FEES': 1931.8, 'APTK': 137.06,
        'RUGR': 130.0, 'SGZH': 1075.0, 'MRKV': 612.0, 'ALRS': 1276.0, 'SELG': 6029.0, 'KLSB': 1220.0, 'LIFE': 615.0,
        'FLOT': 867.5, 'GRNT': 45.550000000000004, 'ENRU': 872.8000000000001, 'GTRK': 371.5, 'SFIN': 4466.0,
        'MGNT': 6315.5, 'SMLT': 4800.2, 'TGKDP': 732.0, 'LNZL': 11550.0, 'RBCM': 414.20000000000005, 'MRKP': 2701.0,
        'LKOH': 7200.0, 'PLZL': 14261.0, 'BSPB': 865.6999999999999, 'UNKL': 8620.0, 'MSST': 212.3, 'TCSG': 7660.0,
        'MGTSP': 1404.0, 'SBER': 3643.7, 'PHOR': 5702.0, 'PRFN': 261.6, 'SVAV': 2260.0, 'UNAC': 715.5, 'IRGZ': 1414.0,
        'AMEZ': 2180.5, 'DSKY': 1346.8000000000002, 'MRKY': 516.0, 'UWGN': 102.6, 'GEMC': 1042.37, 'BELU': 3820.0,
        'NKHP': 3530.0, 'CNTLP': 1011.9999999999999, 'GLTR': 6230.0, 'FIVE': 2388.5, 'BANE': 1534.5, 'OKEY': 456.8,
        'TRMK': 930.8, 'BANEP': 1165.0, 'RUAL': 775.8, 'TTLK': 689.0, 'GMKN': 22864.0, 'MSRS': 1426.0, 'QIWI': 652.0,
        'IRKT': 2430.0, 'ISKJ': 857.6, 'OZON': 3307.0, 'UPRO': 2769.0, 'MTLRP': 3094.0, 'KZOSP': 301.90000000000003,
        'LSNG': 977.0, 'HYDR': 832.0, 'RTKMP': 859.5, 'AFKS': 2791.2, 'VRSB': 2700.0, 'SELGP': 6030.0, 'ROSN': 634.5,
        'NKNC': 1288.0, 'GAZP': 3581.2, 'KRKNP': 15920.0, 'RASP': 4491.0, 'CHMF': 1621.0, 'ETLN': 111.92,
        'RSTIP': 2064.0, 'SBERP': 3330.0, 'POGR': 2415.0, 'GCHE': 3340.0, 'AQUA': 5485.0, 'MSNG': 2329.5,
        'TATNP': 515.9, 'SNGS': 3618.0, 'TGKA': 1124.0, 'MAIL': 1546.0, 'RNFT': 194.8, 'AKRN': 8620.0, 'AGRO': 1192.8,
        'KMAZ': 1216.0, 'OGKB': 723.0, 'RSTI': 1418.1999999999998, 'TATN': 562.5, 'TORS': 3980.0, 'PMSBP': 1560.0,
        'RTKM': 948.4000000000001, 'VSMO': 34000.0, 'MVID': 581.1, 'ROLO': 1010.5, 'PIKK': 1197.0,
        'NLMK': 2254.7999999999997, 'TGKN': 3290.0, 'TRNFP': 156350.0, 'MTSS': 3162.5, 'KROT': 4280.0, 'LSRG': 755.2,
        'SNGSP': 3871.5000000000005, 'NMTP': 795.5, 'MAGN': 702.0999999999999, 'LSNGP': 1729.0, 'LNZLP': 2155.0,
        'SIBN': 5138.0, 'NKNCP': 1047.0, 'DVEC': 1486.0, 'NSVZ': 2005.0, 'RENI': 1150.0, 'TGKBP': 692.0, 'NVTK': 1836.6,
        'TGKD': 750.0, 'MTLR': 162.5, 'RKKE': 7190.0, 'LNTA': 224.4, 'MRKS': 5500.0, 'ORUP': 254.8, 'PMSB': 1653.0,
        'FESH': 2874.0, 'POLY': 1371.0, 'CBOM': 708.0, 'MSTT': 933.5, 'DASB': 333.1, 'MRKC': 432.59999999999997,
        'IRAO': 495.8, 'CNTL': 1386.0, 'AFLT': 679.0, 'ABRD': 2125.0}

sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

# print(sorted_data)
for i in sorted_data:
    print(i[0], i[1])

# candles = find_ticker_price_by("BBG00178PGX3")
# price_data = candles.payload.candles
# print(price_data.pop().c)
