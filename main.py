from bs4 import BeautifulSoup
import requests
import os
import login


username = login.get_username()
password = login.get_password()

session = requests.Session()

payload = {"anchor": "",
           "logintoken": "",
           "username": username,
           "password": password
           }

login_page = session.get("https://ugvle.ucsc.cmb.ac.lk/login/index.php").text
soup_login_page = BeautifulSoup(login_page, 'lxml')

login_form = soup_login_page.find('form', class_='mt-3')

login_token = login_form.find_all('input')[1]['value']

payload["logintoken"] = login_token
# print(payload)

login = session.post(
    "https://ugvle.ucsc.cmb.ac.lk/login/index.php", data=payload)


upcoming_events = session.get(
    "https://ugvle.ucsc.cmb.ac.lk/calendar/view.php?view=upcoming").text
soup_upcoming_events = BeautifulSoup(upcoming_events, 'lxml')

events = soup_upcoming_events.find_all('div', class_='card rounded')

print("\nUpcoming assignments that you have not submitted yet: ")
i = 0
for event in events:
    event_name = event.find('h3').text
    event_link = event.find('a', class_='card-link')['href']

    event_page = session.get(event_link).text
    soup_event_page = BeautifulSoup(event_page, 'lxml')
    event_details = soup_event_page.find_all('td', class_='cell c1 lastcol')
    module_name = soup_event_page.find('h1').text
    due_date = event_details[1].text;
    remaining_time = event_details[2].text;
    submitted = soup_event_page.find_all(
        'td', class_='submissionstatussubmitted cell c1 lastcol')
    if not submitted:
        i += 1
        print()
        print(f'{i}) {module_name} - {event_name}')
        print(f'   - {due_date}')
        print(f'   - {remaining_time}')
        print(f'   - {event_link}')
        print()

# No upcoming assignments
if(i == 0):
    print("You have no upcoming assignments 🎉")

print("\n------------------------------------------------------------")

os.system("pause")
