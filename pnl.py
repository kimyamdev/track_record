import yfinance as yf
import pandas as pd

def pnl(tx_df, startdate, asset_universe, listed_investments, non_listed_investments, custom_prices_df, uk_stocks):

    from datetime import datetime, timedelta

    # Load historical prices of the individual stocks
    two_days_before_start = startdate - timedelta(days = 3)
    quotes = yf.download(tickers=list(listed_investments), start=two_days_before_start, interval="1d")
    df_quotes = quotes['Adj Close'].ffill()
    market_prices = df_quotes[-1:].T
    market_prices = market_prices.reset_index()
    market_prices.columns = ["Asset", "Price"]
    market_prices = market_prices.set_index("Asset")
    market_prices = market_prices.to_dict()["Price"]
    print("market_prices")
    print(market_prices)

    data = custom_prices_df.to_dict('records')

    latest_prices = {}

    for item in data:
        asset = item['Asset']
        price = float(item['Unit Price'])
        if asset not in latest_prices:
            latest_prices[asset] = price
        else:
            latest_prices[asset] = max(latest_prices[asset], price)

    print(latest_prices)

    market_prices.update(latest_prices)

    print("market_prices")
    print(market_prices)

    # create a transactions dataframe with only investments
    transactions = tx_df[tx_df["Class"]=="Investment"]
    transactions["Quantity"] = pd.to_numeric(transactions["Quantity"], errors='coerce')
    transactions["Cost"] = pd.to_numeric(transactions["Cost"], errors='coerce')

    # New dictionary with revised prices
    revised_prices_dict = {}

    # Divide prices by 100 if key ends with ".L"
    for key, value in market_prices.items():
        if key in uk_stocks:
            value = value / 100
        revised_prices_dict[key] = value

    # group the transactions by asset
    grouped_transactions = transactions.groupby("Asset")

    # create a dictionary to store the current market prices for each asset
    market_prices = revised_prices_dict
    print("market prices revised dict")
    print(market_prices)

    # calculate the net profit or loss for each stock
    profits_losses = []
    for asset, transactions in grouped_transactions:
        print(asset)
        sell_transactions = transactions[transactions["Type"]=="SELL"]
        print("### sell_transactions ###")
        print(sell_transactions)
        buy_transactions = transactions[transactions["Type"].isin(["BUY", "IMPORT"])]
        print("### buy_transactions ###")
        print(buy_transactions)
        # calculate the net profit or loss from sell transactions
        sell_profit_loss = (-sell_transactions["Quantity"]*sell_transactions["Cost"]).sum() if not sell_transactions.empty else 0
        print("sell profit loss")
        print(sell_profit_loss)
        # calculate the net profit or loss from buy transactions
        buy_profit_loss = (buy_transactions["Quantity"]*buy_transactions["Cost"]).sum() if not buy_transactions.empty else 0
        print("buy profit loss")
        print(buy_profit_loss)
        # calculate the market value of the remaining shares
        remaining_quantity = buy_transactions["Quantity"].sum() + sell_transactions["Quantity"].sum()
        print("remaining quantity")
        print(remaining_quantity)
        print("market_prices[asset]")
        print(market_prices[asset])
        current_market_value = remaining_quantity * market_prices[asset] if remaining_quantity > 0 else 0
        print("current_market_value")
        print(current_market_value)
        # calculate the total profit or loss
        total_profit_loss = sell_profit_loss - buy_profit_loss + current_market_value
        print("total_profit_loss")
        print(total_profit_loss)
        print("\n")
        # add the result to the list
        profits_losses.append(total_profit_loss)

    print("profits_losses")
    print(profits_losses)

    # create a new dataframe to store the results
    results = pd.DataFrame({"asset": grouped_transactions.groups.keys(), "profits_losses": profits_losses})

    ### EXTRACTING THE LIST OF INVESTMENTS IN ASSET UNIVERSE
    currency_dict = {k: v['Ccy'] for k, v in asset_universe.items() if v['Class'] == 'Investment'}

    asset_fx_prices = {}

    for asset, ccy in currency_dict.items():
        asset_fx_prices[asset] = yf.Ticker(ccy).fast_info["regularMarketPreviousClose"]

    mapped_dict = {}
    for asset in results['asset']:
        if asset in currency_dict:
            ccy = currency_dict[asset]
            mapped_dict[asset] = results.loc[results['asset'] == asset, 'profits_losses'].values[0] * asset_fx_prices[asset]

    sorted_data = dict(sorted(mapped_dict.items(), key=lambda x: x[1], reverse=True))
    print(sorted_data)
    print("total PNL in SGD")
    print(sum(sorted_data.values()))
    return sorted_data