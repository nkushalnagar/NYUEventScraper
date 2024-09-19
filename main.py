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


def correct_url(url):
   if url[0] == 'h':
       return url
   else:
       return 'https://www.events.nyu.edu' + url




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




       # For the top highlighted Event


       feature_top = soup.find_all('div', class_ = 'feature-top')
       for feature in feature_top:
           link = feature.find('a', href = True)['href']
           link = correct_url(link)
           feature = feature.find('div', {'class': 'feature-top-info' })
           event_name = feature.h4.text


           if feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_start_time'}):
               start = feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_start_time'}).text
           else:
               start = None
          
           if feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_end_time'}):
               end = feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_end_time'}).text
           else:
               end = None
           #end = feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_end_time'}).text
           Events.append({'Event Name': event_name,'Date': today, 'Start':start , 'End': end, 'Link': link})


      
       # For other events
       all_events = soup.find_all('div', class_='lw_cal_event')
       n = 1
       for target in all_events:
           title = target.find('div', {'class':'lw_events_title'})
           text = title.a.text
           link = title.a['href']
           link = correct_url(link)
           time_ = target.find('div', {'class':'nyu-date-time'})
          
           if time_.find('span', {'class': 'lw_start_time'}):
               start = time_.find('span', {'class': 'lw_start_time'}).text
           else:
               start = None


           if time_.find('span', {'class': 'lw_end_time'}):
               end = time_.find('span', {'class': 'lw_end_time'}).text
           else:
               end = None


           Events.append({'Event Name': text,'Date': today, 'Start':start , 'End': end, 'Link': link})
           n += 1
       print(f'{n} events for {today}')


       today = today + datetime.timedelta(days=1)
       today_str = conv_date_to_string(today)
       day_of_the_week = day_of_the_week + 1


get_event_pages_for_week()


# Create a DataFrame from the list of events
df = pd.DataFrame(Events)
df.to_csv('file.csv', index=False)
# print(df)
