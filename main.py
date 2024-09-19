import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd




# Set up the WebDriver
driver = webdriver.Chrome()


# Create Events dictionary that will store information about various events throughout the week, this will be eventually converted into a pandas df
Events = []




# Converts datetime package given date structure YYYY-MM-DD to an inputable string
def conv_date_to_string(today_date):
    today_date = str(today_date)
    today_date = today_date.replace('-','')
    return today_date


# Returns specific page link in www.events.nyu.edu page depending on the inputed date string
def correct_url(url):
  if url[0] == 'h':
      return url
  else:
      return 'https://www.events.nyu.edu' + url






# Scrapes nyu events webpages for the week and adds key information about events found to the Events dictionary
def get_event_pages_for_week():
  #Today's date
  today = datetime.date.today()
  today_str = conv_date_to_string(today)


  # Day of the week where 0 represents Monday and 6 represents Sunday
  day_of_the_week = today.weekday()


  # Loops through days of the week accessing each day's events page and adding key information to Events dictionary
  while day_of_the_week <= 6:
     
      # Access webpage
      webpage = "https://events.nyu.edu/day/date/" + today_str
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


          # Scrape start and end time of event
          if feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_start_time'}):
              start = feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_start_time'}).text
          else:
              start = None
        
          if feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_end_time'}):
              end = feature.find('div', {'class': 'nyu-date-time'}).find('span', {'class': 'lw_end_time'}).text
          else:
              end = None
          
          # Add event name, date, start, end, and link for top event to Events dict
          Events.append({'Event Name': event_name,'Date': today, 'Start':start , 'End': end, 'Link': link})




    
      # For other events
      all_events = soup.find_all('div', class_='lw_cal_event')
      n = 1


      for target in all_events:
          # Scrape title
          title = target.find('div', {'class':'lw_events_title'})
          text = title.a.text


          # Scrape link
          link = title.a['href']
          link = correct_url(link)


          # Scrape start and end time
          time_ = target.find('div', {'class':'nyu-date-time'})
        
          if time_.find('span', {'class': 'lw_start_time'}):
              start = time_.find('span', {'class': 'lw_start_time'}).text
          else:
              start = None




          if time_.find('span', {'class': 'lw_end_time'}):
              end = time_.find('span', {'class': 'lw_end_time'}).text
          else:
              end = None


          # Add scraped info to Events dict
          Events.append({'Event Name': text,'Date': today, 'Start':start , 'End': end, 'Link': link})
          n += 1


      # Print how many events occur on certain day to help user's navigate file.csv file better and provide a better understanding of output   
      print(f'{n} events for {today}')


      # Count/move to next day on each iteration of while loop
      today = today + datetime.timedelta(days=1)
      today_str = conv_date_to_string(today)
      day_of_the_week = day_of_the_week + 1


# Call function
get_event_pages_for_week()




# Create a DataFrame from the list of events
df = pd.DataFrame(Events)
df.to_csv('file.csv', index=False)