from flask import Flask, render_template, request
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials

#import libraries
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import os.path
import googleapiclient.discovery
import pandas as pd
from datetime import datetime
from datetime import date

import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from test_gmail_api import send
import json
import math
import numpy as np
import fundamentalanalysis as fa
from assets import listed_investments

# import functions
from report_functions import get_tx_spreadsheet_data, generate_nav_chart_image, \
    get_custom_px_spreadsheet_data, units_history, get_NAV, benchmark_history, \
        send_email, sharpe_ratio, ann_volatility
from historical_positions import historical_portfolio
from twitter_functions import topic_tweets, user_tweets, cluster_tweets
from assets import fx_universe, asset_universe, investments, uk_stocks, listed_investments, non_listed_investments
from pnl import pnl

# import charts

app = Flask(__name__)

api_key = "a1f5ee38358920b130329da9cff2dfde"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reports_form')
def reports_form():
    return render_template('reports_form.html')


@app.route('/twitter_topic_screening', methods=['GET', 'POST'])
def twitter_topic_screening():
    if request.method == 'POST':

        topic = request.form.get('twitter_topic', False)
        num_tweets = request.form.get('num_tweets', False)
        num_clusters = request.form.get('num_clusters', False)
        topic_output = topic_tweets(topic, num_tweets)
        tweet_urls_texts = topic_output['combined_urls_tweets']
        clusters = cluster_tweets(tweet_urls_texts, int(num_clusters))
        clusters = {key: value for key, value in sorted(clusters.items())}
        print(clusters)

        return render_template('twitter_topics.html', topic=topic, clusters=clusters, num_clusters=num_clusters)
    return render_template('twitter_topics.html')

@app.route('/twitter_user_screening', methods=['GET', 'POST'])
def twitter_user_screening():

    if request.method == 'POST':
        user = request.form.get('twitter_user', False)
        print(user)
        num_tweets = request.form.get('num_tweets', False)
        num_clusters = request.form.get('num_clusters', False)
        print(num_clusters)
        user_output = user_tweets(user, num_tweets)
        print(user_output)
        tweet_urls_texts = user_output['combined_urls_tweets']
        print(tweet_urls_texts)
        clusters = cluster_tweets(tweet_urls_texts, int(num_clusters))
        clusters = {key: value for key, value in sorted(clusters.items())}
        print(clusters)

        return render_template('twitter_users.html', user=user, user_output=user_output, clusters=clusters, num_clusters=num_clusters)
    
    return render_template('twitter_users.html')

@app.route('/read_report', methods=['POST'])
def generate_report():

    # Get the URL of the Google spreadsheet from the form data
    spreadsheet_url = request.form['url']

    # Get the tx data from the spreadsheet
    tx_df = get_tx_spreadsheet_data(spreadsheet_url)

    # Get the custom asset prices data from the spreadsheet
    custom_prices_df = get_custom_px_spreadsheet_data(spreadsheet_url)

    # Set report date range
    startdate=tx_df["Date"][1]
    date_range = pd.date_range(start=startdate, end=datetime.today().strftime('%Y-%m-%d'), freq='D')
    # Convert datetime objects to dates
    date_range_no_datetime = [dt.date() for dt in date_range]

    # Build historical portfolio
    hist_ptf_df = historical_portfolio(tx_df = tx_df, custom_prices_df=custom_prices_df)

    # Build today's portfolio
    print("# Current portfolio holdings #")
    p = hist_ptf_df.tail(1).T.reset_index()
    p = p.rename(columns={p.columns[0]: "attr", p.columns[1]: "val"})
    portfolio_today = p.loc[p.attr.str.match('total_position_.*'), :]
    portfolio_today = portfolio_today.sort_values(by="val", ascending=False)
    portfolio_today['Asset'] = portfolio_today['attr'].map(lambda x: x.lstrip('total_position_').rstrip(''))
    portfolio_today = portfolio_today[['Asset', 'val']]
    portfolio_today = portfolio_today.loc[(portfolio_today['val'] > 0)]
    portfolio_today['Asset_Name'] = portfolio_today['Asset'].map({k: v['Name'] for k, v in asset_universe.items()})

    # portfolio_today = portfolio_today.set_index('Asset')
    current_holdings = []
    for k, v in portfolio_today.iterrows():
        print("-", asset_universe[v['Asset']]["Name"], "->", "{:.2%}".format(v['val']))
        current_holdings.append((asset_universe[v['Asset']]["Name"], "{:.2%}".format(v['val'])))

    current_holdings_df = pd.DataFrame(current_holdings, columns=['asset', 'weight'])

    weight_list = current_holdings_df['weight'].tolist()
    weight_list = [float(percentage.strip('%'))/100 for percentage in weight_list]

    holdings = ""
    for a, b in current_holdings:
        text = a + ": " + b
        holdings += "- " + text + "\n"

    # Performance contributors (pnl by asset)

    pnl_by_asset = pnl(tx_df, date_range[0], asset_universe, listed_investments, non_listed_investments, custom_prices_df, uk_stocks)
    print("pnl_by_asset")
    print(pnl_by_asset)

    print(list(pnl_by_asset.values()))
    print(list(pnl_by_asset.values())[0])
    print(type(list(pnl_by_asset.values())[0]))

    # Build units summary
    units_history_df = units_history(tx_df = tx_df, date_range = date_range, hist_ptf_df=hist_ptf_df)

    # Extract list of values for portolio and benchmarks
    list_values_NAV = get_NAV(tx_df = tx_df, date_range = date_range, hist_ptf_df=hist_ptf_df)
    list_values_SP500 = benchmark_history(ticker="SPY", startdate=date_range[0], date_range=date_range)['Price'].tolist()
    
    # generate a correlation matrix between portfolio and benchmark tickers
    benchmark_list = ["ARKK", "SPY", "EEM", "XLE", "LQD", "TLT", "BTC-USD", "ETH-USD", "GLD", "CTA", "REET"]
    corr_data = {'Portfolio': list_values_NAV}
    for ticker in benchmark_list:
        corr_data[ticker] = benchmark_history(ticker=ticker, startdate=date_range[0], date_range=date_range)['Price'].tolist()
    corr_df = pd.DataFrame(corr_data)
    corr_matrix = corr_df.corr().round(2)

    # Generate a chart from an imported function
    nav_chart_path = generate_nav_chart_image(dates = date_range, nav_prices = list_values_NAV)

    # Upcoming earnings

    listed_stocks = [asset for asset in asset_universe.keys() if asset_universe[asset]["Type"] == "Listed_Stock"]
    print(listed_stocks)
    earnings_dates = {}

    for ticker in listed_stocks:
        # Collect recent company quotes
        try:
            quotes = fa.quote(ticker, api_key)
            date = quotes.loc["earningsAnnouncement"]
            try:
                earning_date = datetime.strptime(date[0], '%Y-%m-%dT%H:%M:%S.%f%z')
                earning_date = earning_date.strftime('%Y-%m-%d')
                earnings_dates[ticker] = earning_date
            except: 
                pass
        except:
            print("not found")



    sorted_earnings_dates = dict(sorted(earnings_dates.items(), key=lambda x: x[1]))

    today_str = datetime.today().strftime('%Y-%m-%d')
    today = datetime.strptime(today_str, '%Y-%m-%d').date()

    selected_tickers = {}
    for ticker, date_str in sorted_earnings_dates.items():
        ticker_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if ticker_date >= today:
            selected_tickers[ticker] = ticker_date


    # Send the chart to the user's email
    # send_email(request.form['email'], subject="test subject", body="test body", image_path=nav_chart_path)

    # Send notification to Slack

    # build dictionary for content variables
    dict_vars = {
        "nav_chart_path": nav_chart_path,
        "date_range_no_datetime": date_range_no_datetime,
        "list_values_NAV": get_NAV(tx_df = tx_df, date_range = date_range, hist_ptf_df=hist_ptf_df),
        "list_values_SP500": benchmark_history(ticker="SPY", startdate=date_range[0], date_range=date_range)['Price'].tolist(),
        "cumul_gains": units_history_df['cumul_gains'].tolist(),
        "ptf_volatility": ann_volatility(list_values_NAV),
        "bench_volatility": ann_volatility(list_values_SP500),
        "sharpe_ratio_ptf": sharpe_ratio(list_values_NAV, risk_free_rate=0.04),
        "sharpe_ratio_bench": sharpe_ratio(list_values_SP500, risk_free_rate=0.04),
        "corr_matrix": corr_matrix,
        "corr_list": corr_matrix["Portfolio"].sort_values(ascending=False).drop("Portfolio"),
        "perf_ptf": list_values_NAV[-1] / list_values_NAV[0] - 1,
        "perf_bench": list_values_SP500[-1] / list_values_SP500[0] - 1,
        "today": datetime.today().strftime('%Y-%m-%d'),
        "daily_comments": request.form['comments'],
        "portfolio_name": request.form['portfolio-name'],
        "assets_today": current_holdings_df['asset'].tolist(),
        "assets_weight_today": weight_list,
        "pnl_by_asset": pnl_by_asset,
        "contributors": list(pnl_by_asset.keys()),
        "contributions": list(pnl_by_asset.values()),
        "sorted_earnings_dates": selected_tickers

    }

    # Return a response to the user
    return render_template("report.html", content=dict_vars)


































if __name__ == '__main__':
    app.run(debug=True)
