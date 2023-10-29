#-----------------------------------------------------------------------
# testregdetails.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def run_test(driver, server_url, classid):

    print_flush('-----------------')
    print_flush('classid: ' + classid)
    try:
        driver.get(server_url)
        link_element = driver.find_element(By.LINK_TEXT, classid)
        link_element.click()
        class_details_table = driver.find_element(
            By.ID, 'classDetailsTable')
        print_flush(class_details_table.text)
        course_details_table = driver.find_element(
            By.ID, 'courseDetailsTable')
        print_flush(course_details_table.text)
    except Exception as ex:
        print(str(ex), file=sys.stderr)

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('usage: ' + sys.argv[0] + ' serverURL', file=sys.stderr)
        sys.exit(1)

    server_url = sys.argv[1]
    driver = webdriver.Firefox()

    run_test(driver, server_url, '8321')
    run_test(driver, server_url, '9032')
    run_test(driver, server_url, '1')
    run_test(driver, server_url, 'coursenum')
    run_test(driver, server_url, 'asd;fasd;45')
    run_test(driver, server_url, '10183')
    run_test(driver, server_url, '9012')
    run_test(driver, server_url, '')

    driver.quit()

if __name__ == '__main__':
    main()
