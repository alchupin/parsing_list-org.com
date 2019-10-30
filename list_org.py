import os
import csv

import requests
from bs4 import BeautifulSoup


def _get_html(url):
    """
    Takes url address and returns response's content in Unicode
    :param url: url address: string
    :return: None
    """
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        return r.text
    except:
        None


def _write_csv(data):
    """
    Writes data from dictionary into the file list_org.csv
    :param data: information about company
    :return: None
    """
    if not os.path.isfile('./list_org.csv'):
        with open('list_org.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(
                ('Полное юридическое наименование',
                 'Руководитель',
                 'Дата регистрации',
                 'Статус',
                 'ИНН',
                 'КПП',
                 'ОГРН')
            )
    with open('list_org.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(
            (data['company_name'],
            data['head'],
            data['registration_date'],
            data['status'],
            data['inn'],
            data['kpp'],
            data['ogrn'])
        )


def get_company_info(url):
    company_name = ''
    head = ''
    registration_date = ''
    status = ''
    inn = ''
    kpp = ''
    ogrn = ''

    html_text = _get_html(url)
    soup = BeautifulSoup(html_text, 'lxml')

    try:
        company_name = soup.find_all('div', class_='c2m')[0].find('a').text
    except:
        company_name = 'Информация отсутствует'
    try:
        ogrn = soup.find_all('div', class_='c2m')[2].find_all('p')[3].text.replace('ОГРН: ', '')
    except:
        ogrn = 'Информация отсутствует'

    try:
        table = soup.find('table', class_='tt')
    except:
        pass
    try:
        trs = table.find_all('tr')
    except:
        pass

    if trs:
        for tr in trs:
            tds_all = tr.find_all('td')
            if 'Руководитель' in tds_all[0].text:
                try:
                    head = tds_all[-1].text
                except:
                    head = 'Информация отсутствует'
            if 'ИНН' and 'КПП' in tds_all[0].text:
                try:
                    inn = tds_all[-1].text.split(' ')[0]
                    kpp = tds_all[-1].text.split(' ')[-1]
                except:
                    inn = 'Информация отсутствует'
                    kpp = 'Информация отсутствует'
            if 'Дата регистрации' in tds_all[0].text:
                try:
                    registration_date = tds_all[-1].text.split(' ')[0]
                except:
                    registration_date = 'Информация отсутствует'
            if 'Статус' in tds_all[0].text:
                try:
                    status = tds_all[-1].text
                except:
                    status = 'Информация отсутствует'
    else:
        head = 'Информация отсутствует'
        registration_date = 'Информация отсутствует'
        status = 'Информация отсутствует'
        inn = 'Информация отсутствует'
        kpp = 'Информация отсутствует'
    data = {
        'company_name': company_name,
        'head': head,
        'registration_date': registration_date,
        'status': status,
        'inn': inn,
        'kpp': kpp,
        'ogrn': ogrn
    }

    _write_csv(data)
