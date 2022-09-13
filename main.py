import os
import requests
from datetime import datetime
from twilio.rest import Client


account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
twilio_number = "+18586304318"


stock_api_key = os.environ.get("stock_api_key")



now = datetime.now()
d = now.day-1
day = f"0{d}"

news_response = requests.get(f"https://api.polygon.io/v2/reference/news?ticker=AAPL&published_utc=2022-09-{day}&apiKey={stock_api_key}")
response = requests.get(f"https://api.polygon.io/v1/open-close/AAPL/2022-09-{day}?adjusted=true&apiKey={stock_api_key}")
try:
    news = news_response.json()
    market = response.json()

except ValueError as error_message:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+15598640414",
        from_=twilio_number,
        body=f"Markets were closed yesterday:(\n")
else:

    news_name = news["results"][0]["publisher"]["name"]
    article_title = news["results"][0]["title"]
    content = news["results"][0]["description"]
    url = news["results"][0]["article_url"]
    news_name2 = news["results"][1]["publisher"]["name"]
    article_title2 = news["results"][1]["title"]
    content2 = news["results"][1]["description"]
    url2 = news["results"][1]["article_url"]

    o = market["open"]
    close = market["close"]

    if close > o:
        percent_change = round((close - o) / o * 100)
    else:
        percent_change = round((o - close) / close * 100)

    if percent_change >= 1:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+15598640414",
            from_=twilio_number,
            body=f"AAPL up {percent_change}%\n"
                    f"\n{news_name}\n"
                    f"\nHeadline: {article_title}\n"
                    f"\nBrief: {content}\n")
                    # f"\n{url}\n"
                    # f"\n{news_name2}\n"
                    # f"\nHeadline: {article_title2}\n"
                    # f"\nBrief: {content2}\n"
                    # f"\n{url2}\n")
        print(message.status)

    elif percent_change <= -1:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+15598640414",
            from_=twilio_number,
            body=f"AAPL 🔻 {percent_change}%\n"
                    f"\n{news_name}\n"
                    f"\nHeadline: {article_title}\n"
                    f"\nBrief: {content}\n")
                    # f"\n{url}\n"
                    # f"\n{news_name2}\n"
                    # f"\nHeadline: {article_title2}\n"
                    # f"\nBrief: {content2}\n"
                    # f"\n{url2}\n")
        print(message.status)
    else:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+15598640414",
            from_=twilio_number,
            body=f"AAPL  {percent_change}%\n"
                 f"Slow Day Today")
        print(message.status)

    response.raise_for_status()
