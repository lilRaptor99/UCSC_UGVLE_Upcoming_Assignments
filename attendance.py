from bs4 import BeautifulSoup
import itertools
import threading
import time
import sys

import login


finished_loading = False

# Print loading text on console without blocking the main threads


def print_loading():
    global finished_loading

    for c in itertools.cycle(['|', '/', '-', '\\']):
        if finished_loading:
            break
        sys.stdout.write('\rLoading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone ✔       \n')
    sys.stdout.flush()


# Find all course links
# Visit them one by one to update the last course access time
def mark_attendance(session):
    global finished_loading

    # Finding all course links
    print("Loading course links: ")
    t = threading.Thread(target=print_loading)
    t.start()

    home_page = session.get("https://ugvle.ucsc.cmb.ac.lk/index.php").text
    soup_home_page = BeautifulSoup(home_page, 'lxml')

    all_courses = soup_home_page.find_all(
        'a', class_="list-group-item list-group-item-action")

    course_list = set()
    for course in all_courses:
        course_link = course['href']
        if(course_link.find('course') != -1):
            course_list.add(course_link)

    finished_loading = True
    time.sleep(0.2)
    # print(course_list)

    print("\rVisiting courses: ")
    finished_loading = False
    t = threading.Thread(target=print_loading)
    t.start()

    for course in course_list:
        course_page = session.get(course).text
        soup_course_page = BeautifulSoup(course_page, 'lxml')
        course_title = soup_course_page.find(
            'div', class_="page-header-headings").find('h1').text

        print("\r" + course_title)

    finished_loading = True
    time.sleep(0.2)


if(__name__ == "__main__"):
    print("Testing attendance...")
    session = login.vle_login()
    mark_attendance(session)
