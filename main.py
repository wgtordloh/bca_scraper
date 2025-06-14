import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

company_details = []
def extract_page(company_details, soup):
    titles = soup.find_all("a", class_="title")
    uens = soup.find_all("div", class_="uen")
    addresses = soup.find_all("div", class_="address")
    telephones = soup.find_all("div", class_="tel")
    faxes = soup.find_all("div", class_="fax")

    for title, uen, address, telephone, fax in zip(titles, uens, addresses, telephones, faxes):
        company_details.append({
            "title": title.text.strip(),
            "uen": uen.text.strip(),
            "address": address.text.strip(),
            "telephone": telephone.text.strip(),
            "fax": fax.text.strip()
        })


    for company in company_details:
        print(f"Company Name: {company['title']}")
        print(f"UEN: {company['uen']}")
        print(f"Address: {company['address']}")
        print(f"Telephone: {company['telephone']}")
        print(f"Fax: {company['fax']}")
        print("-" * 40)
    print(f"Total Companies Found: {len(company_details)}")


def main():
    URL = f"https://www1.bca.gov.sg/bca-directory/registered-contractors/construction?workhead=CW01&grading=All&filter=All&itemsperpage=12&page=1"
    driver = webdriver.Chrome()  # Ensure you have the correct WebDriver installed
    driver.get(URL)
    time.sleep(1)  # Wait for the page to load
    next_button = driver.find_element("xpath", "//a[@aria-label='Next']")

    while next_button:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        extract_page(company_details, soup)
        try:
            next_button = driver.find_element("xpath", "//a[@aria-label='Next']")
        except Exception as e:
            print(f"[ERROR] Could not find the 'Next' button: {e}")
            next_button = None
        if next_button:
            next_button.click()
            time.sleep(1)
        else:
            print("[INFO] No more pages to scrape.")
            break
    print("[INFO] Scraping completed.")
    # Save results to CSV
    df = pd.DataFrame(company_details)
    csv_path = os.path.join(os.path.dirname(__file__), "bca_companies.csv")
    df.to_csv(csv_path, index=False)
    print(f"[INFO] Company data saved to: {csv_path}")



    driver.quit()


if __name__ == "__main__":
    main()