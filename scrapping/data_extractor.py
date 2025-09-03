import json
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
from js_simulator import get_html_after_js

# Global Variables
URL_template = (
    "https://www.agoda.com/flights/results?departureFrom=PNQ&departureFromType=1&arrivalTo=NAG&arrivalToType=1"
    "&departDate={datedept}"
    "&returnDate={dateretn}"
    "&searchType=1&cabinType=Economy&adults=1&"
)

def date_generator(end: str = None) -> list:
    """
    create list of dates from today till next year same date
    """
    dates = []
    start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    if end:
        end_date = datetime.strptime(end, "%d/%m/%Y")
    else:
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
    data_dict = {}  # key: date, value: html_content
    for i in dates:
        try:
            dep_date = i.strftime("%Y-%m-%d")
            ret_date = (i + timedelta(days=1)).strftime("%Y-%m-%d")
            url = URL_template.format(datedept=dep_date, dateretn=ret_date)
            html = BeautifulSoup(get_html_after_js(url), "html.parser")
            data_dict[dep_date] = [tag.find_parent('div', class_=re.compile(r'^GridItem__')) for tag in html.find_all('span', {'data-testid': 'duration'})]

        except Exception as e:
            print(e)
            continue

    return data_dict

def extract_details(dates: list) -> dict:
    content_dict = content(dates)
    data_dict = {} # Key: date, Value: list -> list -> Airline, Departure_Arrival_Time, Duration, Stops, Price

    # Regex patterns
    departure_arrival_Time = r'role="presentation">(.*?)<'
    duration = r'<span class="sc-hLseeU Typographystyled__TypographyStyled-sc-1uoovui-0 ehiMbI jFZsPx" data-testid="duration">(.*?)</span>'
    price = r'>(.*?)</span></div></div></span>'
    stops = r'</div></div></div><p class="body-sm text-secondary">(.*?)</p></div>'

    for i in content_dict.keys():
        date_list = []
        for j in content_dict[i]:
            metadata = [] # Temporary list to hold the data

            # Pattern matching to find the required data, using both BeautifulSoup and Regex
            AIRLINE_tag = j.find('p', class_="iYbjBz")
            AIRLINE = AIRLINE_tag.get_text(strip=True) if AIRLINE_tag else "N/A" # BeautifulSoup

            DEPARTURE_ARRIVAL_TIME = re.findall(departure_arrival_Time, str(j)) # regex

            DURATION_tag = j.find('span', {'data-testid': 'duration'})
            DURATION = DURATION_tag.get_text(strip=True) if DURATION_tag else "N/A" # BeautifulSoup

            PRICE_tag = j.find('div', {'dir':"ltr"})
            PRICE = PRICE_tag.get_text(strip=True) if PRICE_tag else "N/A" # BeautifulSoup

            # Appending the singular flight data into the temporary list
            metadata.append(AIRLINE)
            metadata.append(DEPARTURE_ARRIVAL_TIME)
            metadata.append(DURATION)
            metadata.append(PRICE)

            # Appending the metadata of each flight into the main list
            date_list.append(metadata)

        data_dict[i] = date_list

    return data_dict