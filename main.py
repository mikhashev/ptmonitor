
from openapi_client import openapi



def get_token():
    """
    get token locate locally and connect to api
    :return: client
    """

    with open('my_ti_token.txt', "r") as file:
        token = file.read()




    return token


client = openapi.api_client(get_token())

def get_stocks_to_list():
    """
    get two stock lists

        {'currency': 'USD',
      'figi': 'BBG001WTBC36',
      'isin': 'US7374461041',
      'lot': 1,
      'min_price_increment': 0.01,
      'name': 'Post Holdings Inc',
      'ticker': 'POST',
      'type': 'Stock'},

    :return: list[list, list]
    """

    stocks = client.market.market_stocks_get()

    instr_list = stocks.payload.instruments

    russian_stocks = []
    foreign_stocks = []
    for stock in instr_list:
        ticker_name = stock.ticker
        ticker_currency = stock.currency

        # classification by currency
        if ticker_currency == 'RUB':
            russian_stocks.append(ticker_name)

        elif ticker_currency == 'USD':
            foreign_stocks.append(ticker_name)

    # print('Русские акции: ', len(russian_stocks))
    # print(russian_stocks)
    # print('Иностранные акции: ', len(foreign_stocks))
    # print(foreign_stocks)

    return russian_stocks, foreign_stocks


def get_figi_by_ticker(ticker) -> str:


    ticker_data = client.market.market_search_by_ticker_get(ticker)  # get ticker by figi

    figi_data = ticker_data.payload.instruments[0]
    figi = figi_data.figi
    return figi

def get_orderbook(ticker = str("MAIL"), depth = int(900)):



    orderbook_data = client.market.market_orderbook_get_with_http_info(get_figi_by_ticker(ticker), depth)

    orderbook_data = orderbook_data[0]
    orderbook_data = (orderbook_data.payload)

    asks_price_total = float()
    asks_quantity_total = int()
    bids_price_total = float()
    bids_quantity_total = int()


    print(len(orderbook_data.asks))
    print(orderbook_data.asks)


    for ask_bid in orderbook_data.asks:

        asks_quantity_total += ask_bid.quantity
        asks_price_total += ask_bid.price * ask_bid.quantity

    print(len(orderbook_data.bids))
    print(orderbook_data.bids)

    for bid in orderbook_data.bids:

        bids_quantity_total += bid.quantity
        bids_price_total += bid.price * bid.quantity

    # 'close_price': 15313.0,
    # 'depth': 900,
    # 'face_value': None,
    # 'figi': 'BBG000R607Y3',
    # 'last_price': 15790.5,
    # 'limit_down': 14234.5,
    # 'limit_up': 16418.5,
    # 'min_price_increment': 0.5,
    # 'trade_status': 'NormalTrading'}

    print('\nclose_price: ',orderbook_data.close_price)
    print('last_price: ', orderbook_data.last_price)
    print('limit_up: ', orderbook_data.limit_up)
    print('limit_down: ', orderbook_data.limit_down)
    print('min_price_increment: ', orderbook_data.min_price_increment)

    print("\nasks_price_total:", asks_price_total)
    print("asks_quantity_total:", asks_quantity_total)

    print("bids_price_total:", bids_price_total)
    print("bids_quantity_total:", bids_quantity_total)
#print(client.market.market_stocks_get())

#print(client.market.market_search_by_ticker_get("BANE"))
get_orderbook()