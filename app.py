from flask import Flask, render_template, request
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import os.path
import googleapiclient.discovery
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from functions import get_spreadsheet_data, generate_chart_image, send_email
from test_gmail_api import send
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-report', methods=['POST'])
def generate_report():
    # Get the URL of the Google spreadsheet from the form data
    spreadsheet_url = request.form['url']

    # Get the data from the spreadsheet
    df = get_spreadsheet_data(spreadsheet_url)

    print(df)

    # Generate the chart
    chart_path = generate_chart_image(df)

    # Send the chart to the user's email
    # send_email(request.form['email'], subject="test subject", body="test body", image_path=chart_path)

    # Return a response to the user
    return render_template("report.html")



if __name__ == '__main__':
    app.run(debug=True)
