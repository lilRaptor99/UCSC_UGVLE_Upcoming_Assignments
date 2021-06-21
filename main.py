from bs4 import BeautifulSoup
import requests
import os
import platform

import login
import attendance


session = login.vle_login()

attendance.mark_attendance(session)


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

    due_date = "N/A"
    remaining_time = "N/A"
    if(len(event_details) > 2):
        due_date = event_details[1].text
        remaining_time = event_details[2].text

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

if(platform.system() == 'Windows'):
    os.system("pause")
else:
    input("Press return/enter to exit: ")
