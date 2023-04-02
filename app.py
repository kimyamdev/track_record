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
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from test_gmail_api import send
import json

# import functions
from functions import get_tx_spreadsheet_data, generate_nav_chart_image, \
    get_custom_px_spreadsheet_data, units_history, get_NAV, send_email
from historical_positions import historical_portfolio

# import charts

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-report', methods=['POST'])
def generate_report():
    # Get the URL of the Google spreadsheet from the form data
    spreadsheet_url = request.form['url']

    # Get the tx data from the spreadsheet
    tx_df = get_tx_spreadsheet_data(spreadsheet_url)
    print(tx_df)

    # Get the custom asset prices data from the spreadsheet
    custom_prices_df = get_custom_px_spreadsheet_data(spreadsheet_url)
    print(custom_prices_df)

    # Set report date range
    startdate=tx_df["Date"][1]
    date_range = pd.date_range(start=startdate, end=date.today(), freq='D')
    # Convert datetime objects to dates
    date_range_no_datetime = [dt.date() for dt in date_range]

    print("DATE RANGE IN APP.PY")
    print(date_range)
    print("###############")

    # Build historical portfolio
    hist_ptf_df = historical_portfolio(tx_df = tx_df, custom_prices_df=custom_prices_df)

    # Build units summary
    units_history_df = units_history(tx_df = tx_df, date_range = date_range, hist_ptf_df=hist_ptf_df)

    # Build portfolio NAV
    list_values_NAV = get_NAV(tx_df = tx_df, date_range = date_range, hist_ptf_df=hist_ptf_df)

    # Generate the chart
    nav_chart_path = generate_nav_chart_image(dates = date_range, nav_prices = list_values_NAV)

    # Send the chart to the user's email
    # send_email(request.form['email'], subject="test subject", body="test body", image_path=nav_chart_path)

    # build dictionary for content variables

    dict_vars = {
        "nav_chart_path": nav_chart_path,
        "date_range_no_datetime": date_range_no_datetime,
        "list_values_NAV": list_values_NAV
    }

    # Return a response to the user
    return render_template("report.html", content=dict_vars)

if __name__ == '__main__':
    app.run(debug=True)
