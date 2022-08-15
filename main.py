# Import libraries needed
import csv
from bs4 import BeautifulSoup as bsoup
from selenium import webdriver
import time

# Get information from each container
def extract_record(container):
    name = container.h2.a.span.text

    try:
        price = container.find('span', 'a-price').find('span','a-offscreen').text
    except AttributeError:
        price = ''

    try:
        ratings = container.i.text
        n_ratings = container.find('span', {'class' : 'a-size-base s-underline-text'}).text
    except AttributeError:
        ratings = ''
        n_ratings = ''

    website = 'https://amazon.co.uk' + container.h2.a.get('href')

    return (name, price, ratings, n_ratings, website)

def main():
    # Run chrome on software
    driver = webdriver.Chrome('C:/Users/Bing En/chromedriver.exe')
    url = 'https://www.amazon.co.uk/s?k=gaming+chair&crid=2HPJT74CFLGNR&sprefix=gaming+chai%2Caps%2C166&ref=nb_sb_noss_2'
    records = []
    # Run for 20 pages
    for i in range(20):
        driver.get(url)
        # Use beautiful soup on HTML text
        soup = bsoup(driver.page_source, 'lxml')
        # Get container of each  item
        containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        for container in containers:
            record = extract_record(container)
            if record:
                records.append(record)

        # Find the URL to the next page
        pages =  soup.find('span', {'class': 's-pagination-strip'})
        try:
            next_page =  pages.find('a', {'class' : 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href']
        except TypeError:
            next_page = None
        # Stop the loop if we reached the end before 20 pages
        if not next_page:
            break
        url = 'https://amazon.co.uk' + next_page

    driver.close()

    # Save data to csv
    with open('results.csv', 'w',newline = '',encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Price', 'Rating', 'Review Count' , 'URL'])
        writer.writerows(records)

if __name__ == '__main__':
    main()
