import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


# Set up the WebDriver
driver = webdriver.Chrome()


Events = []


# Get event pages for the week until Sunday
def conv_date_to_string(today_date):
   today_date = str(today_date)
   today_date = today_date.replace('-','')
   return today_date


def get_event_pages_for_week():
   today = datetime.date.today()
   day_of_the_week = today.weekday()
   today_str = conv_date_to_string(today)
   print(day_of_the_week)
   while day_of_the_week <= 6:
       webpage = "https://events.nyu.edu/day/date/" + today_str
       print(webpage)


       driver.get(webpage)

       time.sleep(1)
       # Parse the page source with Beautiful Soup
       soup = BeautifulSoup(driver.page_source, 'html.parser')


       target_titles = soup.find_all('div', class_='lw_events_title')

       feature_top = soup.find_all('div', class_ = 'feature-top-info')
       for feature in feature_top:
           feature_top_header = feature.h4.text
       Events.append({'Event Name': feature_top_header,'Date': today})
       n = 1


       for target in target_titles:
           text = target.a.text
           Events.append({'Event Name': text, 'Date': today})  ############ need to add more items here #########
           n += 1

       event_date_time = soup.find_all('div', class_ = 'nyu-date-time')

       for date_time in event_date_time:
           start = ""
           end = ""
           end = date_time.find_all('span', class_ = 'lw_end_time')
           start = date_time.find_all('span', class_ = 'lw_start_time')
           Events.append({'Start Time': start, 'End Time': end})

       print(f'{n} events for {today}')


       today = today + datetime.timedelta(days=1)
       today_str = conv_date_to_string(today)
       day_of_the_week = day_of_the_week + 1


get_event_pages_for_week()


# Create a DataFrame from the list of events
df = pd.DataFrame(Events)
print(df)