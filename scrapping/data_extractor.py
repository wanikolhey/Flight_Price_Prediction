# import pandas as pd
import json
import requests
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
from js_simulator import get_html_after_js

# Global Variables
URL_template = (
    "https://www.ixigo.com/search/result/flight"
    "?from=PNQ&to=NAG&date={date}"
    "&adults=1&children=0&infants=0&class=e&source=Search+Form&utm_source=Brand_Ggl_Search&utm_medium=paid_search_google"
)

def date_generator() -> list:
    """
    create list of dates from today till next year same date
    """
    dates = []
    start_date = datetime.today()
    end_date = start_date + timedelta(days=365)
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)

    return dates

def content(dates: list) -> dict:
    """
    create url for each date in dates list
    """
    pattern = r'<div class="flex items-start w-full">(.*?)</button></div></div></div></div>'
    data_dict = {}  # key: date, value: html_content
    for i in dates:
        try:
            dep_date = i.strftime("%d%m%Y")
            url = URL_template.format(date=dep_date)
            html = BeautifulSoup(get_html_after_js(url), "html.parser")
            data_dict[dep_date] = re.findall(pattern, str(html))

        except Exception as e:
            print(e)
            continue

    return data_dict

def extract_details(dates: list) -> dict:
    content_dict = content(dates)
    data_dict = {"testdate": [["metadata1"],["metadata2"]]} # Key: date, Value: list -> list -> Airline, Departure_Arrival_Time, Duration, Stops, Price

    # Regex patterns
    airline = r'<p class="body-md text-primary truncate max-w-125 airlineTruncate font-medium">(.*?)</p>'
    departure_arrival_Time = r'<h6 class="h6 text-primary font-medium">(.*?)</h6>'
    duration = r'<div class="text-center"><p class="body-sm text-secondary">(.*?)</p><div'
    price = r'<h6 data-testid="pricing" class="h6 text-primary font-bold">(.*?)</h6>'
    stops = r'<div class="flex justify-evenly w-full absolute"></div></div><p class="body-sm text-secondary">(.*?)</p></div>'

    for i in content_dict.keys():
        date_list = []
        for j in content_dict[i]:
            metadata = []
            AIRLINE = re.findall(airline, str(j))
            DEPARTURE_ARRIVAL_TIME = re.findall(departure_arrival_Time, str(j))
            DURATION = re.findall(duration, str(j))
            PRICE = re.findall(price, str(j))
            STOP_LIST = re.findall(stops, str(j))
            metadata.append(AIRLINE)
            metadata.append(DEPARTURE_ARRIVAL_TIME)
            metadata.append(DURATION)
            metadata.append(PRICE)
            metadata.append(STOP_LIST)

            date_list.append(metadata)

        data_dict[i] = date_list

    return data_dict

if __name__ == "__main__":
    dates = date_generator()
    data_dict = extract_details(dates)
    with open("data_dict.json", "w", encoding="utf-8") as f:
        json.dump(data_dict, f)

