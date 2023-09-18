#Imports / Importaciones
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

# Configure options and initialize Chrome browser / Configura las opciones y inicializa el navegador Chrome
chromedriver_path = r'' # Chromedriver path
s = Service(chromedriver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=s, options=options)
URL = 'https://elcheparqueempresarial.es/epe-listado-por-categoria/listado-completo-de-empresas/'
driver.get(URL)
sleep(3) 

# CSV file where the data will be saved / Archivo CSV donde se guardarán los datos
file_name = 'listado_de_empresas_elche.csv'
with open(file_name, 'w', newline='', encoding='utf-8') as file_csv:
    csv_writer = csv.writer(file_csv)
    csv_writer.writerow(['Empresa', 'Telefono', 'Email', 'Web'])

# Loop for navigating and extracting company data / Bucle que recorre las páginas y extrae datos de las empresas
    while True:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        companies = soup.find_all('div', class_='atbd_single_listing')

        for company in companies:
            name = company.find('h4', class_='atbd_listing_title').a.get_text()
            phone_element = company.find('span', class_='la-phone')
            phone = phone_element.find_next('a').get_text().strip() if phone_element else 'No disponible'
            email_element = company.find('span', class_='la-envelope')
            email = email_element.find_next('a').get_text().strip() if email_element else 'No disponible'
            web_element = company.find('span', class_='la-globe')
            web = web_element.find_next('a').get('href').strip() if web_element else 'No disponible'

            csv_writer.writerow([name, phone, email, web])

        # Try to find and click the "Next" button to move to the next page
        # Intenta encontrar y hacer clic en el botón "Siguiente" para avanzar a la siguiente página
        try:
            next_button = driver.find_element(By.CLASS_NAME, 'next')
            next_page_link = next_button.get_attribute('href')
            if next_page_link:
                driver.get(next_page_link)
                sleep(1)
        except NoSuchElementException:
            break

print(f'Los datos se han guardado en "{file_name}"')
driver.quit()