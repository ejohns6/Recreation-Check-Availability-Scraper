import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def MonthConversion(Mon):
    if Mon.startswith('Jan'):
        return '01'
    elif Mon.startswith('Feb'):
        return '02'
    elif Mon.startswith('Mar'):
        return '03'
    elif Mon.startswith('Ap'):
        return '04'
    elif Mon.startswith('May'):
        return '05'
    elif Mon.startswith('Jun'):
        return '06'
    elif Mon.startswith('Jul'):
        return '07'
    elif Mon.startswith('Aug'):
        return '08'
    elif Mon.startswith('Sept'):
        return '09'
    elif Mon.startswith('Oct'):
        return '10'
    elif Mon.startswith('Nov'):
        return '11'
    elif Mon.startswith('Dec'):
        return '12'


options = webdriver.ChromeOptions()
options.add_argument('headless')

url = 'https://www.recreation.gov/camping/campgrounds/232507/availability'
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Chrome()
driver.get(url)

for i in range(6):
    #driver.find_element_by_xpath("//@class='rec-button-tertiary-alt.load-more-btn']").click()
    #WebDriverWait(driver, 10).until_not(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, '.rec-button-tertiary-alt.load-more-btn')))
    #driver.find_element(By.CSS_SELECTOR, '.rec-button-tertiary-alt.load-more-btn').click()
    driver.find_element(By.CSS_SELECTOR, '.rec-button-tertiary-alt.load-more-btn').send_keys(Keys.ENTER)


Lists_Of_Dates = []
availabilityTable = []
site_Count = 0

for i in range(12):
    if i != 0:
        driver.find_element(By.XPATH, "//*[@id='rec-campground-availability-title']/div[3]/div[2]/button[4]").send_keys(Keys.ENTER)
        driver.find_element(By.XPATH, "//*[@id='rec-campground-availability-title']/div[3]/div[2]/button[4]").send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until_not(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, '.rec-table-overlay')))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    tableDates = soup.find('table', attrs={'id': "availability-table", 'class': 'campsite-availability-table'}).find('thead')
    tableAvailability = soup.find('table', attrs={'id': "availability-table", 'class': 'campsite-availability-table'}).find('tbody')
    #print(tableDates.prettify())
    #print('\n\n\n')
    #print(tableAvailability.prettify())

    for row in tableDates.findAll('tr')[1:]:
        for cell in row.findAll('th'):
            if i == 0:
                if cell.find('span', attrs={'class': 'title'}):
                    cellTitle = cell.find('span', attrs={'class': 'title'})
                    #print(cellTitle.text)
                    Lists_Of_Dates.append(cellTitle.text)
                else:
                    cellTitle = cell.find('button')
                    #print(cellTitle['aria-label'])
                    cellTitleSplit = cellTitle['aria-label'].rstrip().split(', ')
                    MonthDate = cellTitleSplit[1].split(' ')
                    if int(MonthDate[1]) < 10:
                        MonthDayYear = str(MonthConversion(MonthDate[0])) + "-0" + str(MonthDate[1]) + "-" + str(cellTitleSplit[2])
                        #print(MonthDayYear)
                        Lists_Of_Dates.append(MonthDayYear)
                    else:
                        MonthDayYear = str(MonthConversion(MonthDate[0])) + "-" + str(MonthDate[1]) + "-" + str(cellTitleSplit[2])
                        #print(MonthDayYear)
                        Lists_Of_Dates.append(MonthDayYear)
            else:
                if cell.find('span', attrs={'class': 'title'}):
                    continue
                else:
                    cellTitle = cell.find('button')
                    #print(cellTitle['aria-label'])
                    cellTitleSplit = cellTitle['aria-label'].rstrip().split(', ')
                    MonthDate = cellTitleSplit[1].split(' ')
                    if int(MonthDate[1]) < 10:
                        MonthDayYear = str(MonthConversion(MonthDate[0])) + "-0" + str(MonthDate[1]) + "/" + str(cellTitleSplit[2])
                        #print(MonthDayYear)
                        Lists_Of_Dates.append(MonthDayYear)
                    else:
                        MonthDayYear = str(MonthConversion(MonthDate[0])) + "-" + str(MonthDate[1]) + "-" + str(cellTitleSplit[2])
                        #print(MonthDayYear)
                        Lists_Of_Dates.append(MonthDayYear)

    for row in tableAvailability.findAll('tr'):
        if i == 0:
            availabilityTable_Row = []
            CampSite = row.find('button', attrs={'class': 'rec-availability-item'})
            #print(CampSite.text)
            availabilityTable_Row.append(CampSite.text)

            for cell in row.findAll('td'):
                if cell.find('button', attrs={'class': 'rec-availability-date'}):
                    availability = cell.find('button', attrs={'class': 'rec-availability-date'})
                    #print(availability.text)
                    if(availability.text != "A"):
                        availabilityTable_Row.append('X')
                    else:
                        availabilityTable_Row.append(availability.text)

                else:
                    #print(cell.text)
                    availabilityTable_Row.append(cell.text)
            availabilityTable.append(availabilityTable_Row)
        else:
            #print(site_Count)
            for cell in row.findAll('td'):
                if cell.find('button', attrs={'class': 'rec-availability-date'}):
                    availability = cell.find('button', attrs={'class': 'rec-availability-date'})
                    #print(availability.text)
                    if (availability.text != 'A'):
                        availabilityTable[site_Count].append('X')
                    else:
                        availabilityTable[site_Count].append(availability.text)

        site_Count += 1

    site_Count = 0


#print(availabilityTable)
#print(Lists_Of_Dates)

driver.close()


outputFile = open("AssateagueAvailability.csv", "w")
writer = csv.writer(outputFile, lineterminator='\n')
writer.writerow(Lists_Of_Dates)
writer.writerows(availabilityTable)
outputFile.close()
