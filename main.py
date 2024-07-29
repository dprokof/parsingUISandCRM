import time

import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool


def get_projectnames():
    projectnames = []
    time.sleep(0.01)
    responsedata = requests.get('<url from CRM method>',verify=False, allow_redirects=True, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    if responsedata.status_code == 200:
        responsedata = responsedata.json()
        for elem in responsedata['result']:
            projectnames.append(elem)
    return projectnames


def get_data(projectname):
    try:
        service = ChromeService(executable_path='/home/dprokof/PycharmProjects/parsingEICandCRM/chromedriver')
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = Chrome(service=service, options=options)
        action = ActionChains(driver)
        driver.get('https://zakupki.gov.ru/epz/main/public/home.html')
        driver.set_page_load_timeout(10)
        try:
            driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[4]/div/div[1]/div/button').click()
        except NoSuchElementException:
            pass
        search = driver.find_element(by=By.CLASS_NAME, value='search__input')
        search.click()
        search.send_keys(projectname)
        driver.find_element(by=By.CLASS_NAME, value='search__btn').click()
        time.sleep(1)
        projectname = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
                                                             '/div/div/div[1]/div[3]/div/div[1]'
                                                             '/div[1]/div[1]/div/div[1]/a').text
        projectname = projectname.replace('№ ', '')
        # print("Номер извещения: ", projectname)
        order_status = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
                                                              '/div/div/div[1]/div[3]/div/div'
                                                              '/div[1]/div[1]/div[2]/div[2]').text
        # print("Статус извещения: ", order_status)
        start_amount = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
                                                              '/div/div/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[2]')
        search = start_amount
        start_amount = start_amount.text
        start_amount = start_amount.replace(' ', '').replace('₽', '').replace(',', '.')
        start_amount = float(start_amount)
        # print("Начальная сумма: ", start_amount)
        action.move_to_element(search)
        action.perform()
        time.sleep(1)
        try:
            driver.find_element(by=By.LINK_TEXT, value='Контракт').click()
            time.sleep(1)
            driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
                                                   '/div/div/div[1]/div[3]/div/div/div[2]/div[3]/div[2]/a').click()
        except NoSuchElementException:
            # print('На данный момент нет контракта по этому извещению')
            driver.quit()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        date_sign = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
                                                           '/div/div/div[1]/div[3]/div/div[1]/div[2]'
                                                           '/div[2]/div[2]').text
        # print("Дата заключения контракта: ", date_sign)
        date_off = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
                                                          '/div/div/div[1]/div[3]/div/div[1]/div[2]/div[2]/div[4]').text
        # print("Срок исполнения: ", date_off)
        date_registr = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
                                                              '/div/div/div[1]/div[3]'
                                                              '/div/div[1]/div[2]/div[2]/div[5]/div[1]/div[2]').text
        # print("Размещено в регистре контрактов: ", date_registr)
        update_registr = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]/div/div/div[1]'
                                                                '/div[3]/div/div[1]'
                                                                '/div[2]/div[2]/div[5]/div[2]/div[2]').text
        # print("Обновлено в реестре контрактов: ", update_registr)
        customer_name = driver.find_element(by=By.XPATH, value='/html/body/form/section[2]/div/div/div[1]'
                                                               '/div[3]/div/div[1]/div[1]/div[2]/div[1]/div[2]/a').text
        # print("Заказчик контракта: ", customer_name)
        # driver.find_element(by=By.XPATH, value='/html/body/form/section[2]'
        #                                        '/div/div/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[1]/a').click()
        driver.find_element(by=By.XPATH, value='/html/body/form/section[2]/div/div/div[1]'
                                               '/div[3]/div/div[1]/div[1]/div[1]/div/div[1]/a').click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[3])
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]').click()
        contract_number = driver.find_element(by=By.XPATH, value='/html/body/div[2]'
                                                                 '/div/div[1]/div[2]'
                                                                 '/div[2]/div[1]/div[1]/div/span[1]/a').text
        contract_number = contract_number.replace('№ ', '')
        # print("Номер контракта: ", contract_number)
        contract_status = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[1]'
                                                                 '/div[2]/div[2]/div[1]/div[1]/div/span[2]').text
        # print("Статус контракта: ", contract_status)
        contract_amount = driver.find_element(by=By.XPATH, value='/html/body/div[2]'
                                                                 '/div/div[1]/div[2]/div[2]/div[2]/div[1]/span[2]').text
        contract_amount = contract_amount.replace(' ', '').replace('₽', '').replace(',', '.')
        contract_amount = float(contract_amount)
        # print("Сумма контракта: ", contract_amount)
        time.sleep(5)
        y_r = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[1]/div[3]/div/a[3]')
        if y_r.text.lower() == 'исполнение (расторжение) контракта':
            y_r.click()
            time.sleep(1)
            amount_executed = driver.find_element(by=By.XPATH, value='/html/body/div[2]'
                                                                     '/div/div[2]/div[2]'
                                                                     '/div/div/div/div/div'
                                                                     '/table/tbody/tr[1]/td[3]').text
            amount_executed = float(amount_executed.replace(' ', '').replace(',', '.'))
            # print('Стоимость исполненных обязательств: ', amount_executed)
            amount_actually_paid = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[2]'
                                                                          '/div[2]/div/div/div/div/div/'
                                                                          'table/tbody/tr[1]/td[4]').text
            amount_actually_paid = float(amount_actually_paid.replace(' ', '').replace(',', '.'))
            # print("Фактически оплачено: ", amount_actually_paid)
        else:
            amount_executed = 'На данный момент нет документов по исполнению контракта'
            amount_actually_paid = 'На данный момент нет документов по исполнению контракта'

        data_frame = {
            'projectname': projectname,
            'order_status': order_status,
            'start_amount': start_amount,
            'date_sign': date_sign,
            'date_off': date_off,
            'date_registr': date_registr,
            'update_registr': update_registr,
            'customer_name': customer_name,
            'contract_number': contract_number,
            'contract_status': contract_status,
            'contract_amount': contract_amount,
            'amount_executed': amount_executed,
            'amount_actually_paid': amount_actually_paid
        }

        header = {
            'Content-Type': 'application/json'
        }
        try:
            requests.post(<'url from CRM>', headers=header, json=data_frame)
        except Exception as ex:
            print(ex)
        print(data_frame)
        driver.quit()
    except Exception as ex:
        pass


if __name__ == '__main__':
    projectnames = get_projectnames()
    p = Pool(processes=2)
    p.map(get_data, projectnames)
