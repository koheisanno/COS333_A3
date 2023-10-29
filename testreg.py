#-----------------------------------------------------------------------
# testreg.py
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

def run_test(driver, input_values):

    print_flush('-----------------')
    for key, value in input_values.items():
        print_flush(key + ': |' + value + '|')

    if 'dept' in input_values:
        dept_input = driver.find_element(By.ID, 'deptInput')
        dept_input.send_keys(input_values['dept'])
    if 'coursenum' in input_values:
        coursenum_input = driver.find_element(By.ID, 'coursenumInput')
        coursenum_input.send_keys(input_values['coursenum'])
    if 'area' in input_values:
        area_input = driver.find_element(By.ID, 'areaInput')
        area_input.send_keys(input_values['area'])
    if 'title' in input_values:
        title_input = driver.find_element(By.ID, 'titleInput')
        title_input.send_keys(input_values['title'])

    submit_button = driver.find_element(By.ID, 'submitButton')
    submit_button.click()

    overviews_table = driver.find_element(By.ID, 'overviewsTable')
    print_flush(overviews_table.text)

    if 'dept' in input_values:
        dept_input = driver.find_element(By.ID, 'deptInput')
        dept_input.clear()
    if 'coursenum' in input_values:
        coursenum_input = driver.find_element(By.ID, 'coursenumInput')
        coursenum_input.clear()
    if 'area' in input_values:
        area_input = driver.find_element(By.ID, 'areaInput')
        area_input.clear()
    if 'title' in input_values:
        title_input = driver.find_element(By.ID, 'titleInput')
        title_input.clear()

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('usage: ' + sys.argv[0] + ' serverURL', file=sys.stderr)
        sys.exit(1)

    server_url = sys.argv[1]

    driver = webdriver.Firefox()
    driver.get(server_url)

    run_test(driver, {'dept':'COS'})
    run_test(driver,   {'dept':'COS', 
                        'coursenum':'2', 
                        'area':'qr', 
                        'title':'intro'})
    run_test(driver, {'dept':'COS', 
                      'coursenum':'2',
                      'area':'qR', 
                      'title':'iNtR'})

    run_test(driver, {})
    run_test(driver, {'title': ' Introduction'})
    run_test(driver, {'title': 'Introduction'})
    run_test(driver, {'title': '  Introduction'})
    run_test(driver, {'title': 'Introduction '})
    run_test(driver, {'title': 'Introduction  '})
    run_test(driver, {'dept': '  '})
    run_test(driver, {'dept': ' '})
    run_test(driver, {'dept': ''})
    run_test(driver, {'dept': 'aAs'})
    run_test(driver, {'dept': 'Aa'})
    run_test(driver, {'coursenum': '23.4'})
    run_test(driver, {'coursenum': '134'})
    run_test(driver, {'title': 'Independent Study'})
    run_test(driver, {'title': 'Independent Study '})
    run_test(driver, {'title': 'Independent Study  '})
    run_test(driver, {'title': ' Independent Study'})
    run_test(driver, {'title': '  Independent Study'})
    run_test(driver, {'area': '56'})
    run_test(driver, {'area': '56f.3'})
    run_test(driver, {'title': '34asdfa'})





    driver.quit()

if __name__ == '__main__':
    main()
