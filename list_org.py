import os
import csv
from typing import Optional

import requests
from bs4 import BeautifulSoup


def _get_html(url: str) -> Optional[str]:
    """
    Takes url address and returns response's content in Unicode
    :param url: url address: string
    :return: string if url available or None otherwise
    """
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        return r.text
    except:
        return None


def _write_csv(data: dict) -> None:
    """
    Writes data from dictionary into the file list_org.csv
    :param data: information about company, dictionary
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


def get_company_info(url: str):
    """
    Takes url address and writes information about company into the file list_org.csv
    :param url: string
    :return: None
    """
    info_n_a = "Информация отсутствует"

    html_text = _get_html(url)
    soup = BeautifulSoup(html_text, 'lxml')

    try:
        company_name = soup.find_all('div', class_='c2m')[0].find('a').text
    except:
        company_name = info_n_a
    try:
        ogrn = soup.find_all('div', class_='c2m')[2].find_all('p')[3].text.replace('ОГРН: ', '')
    except:
        ogrn = info_n_a

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
                    head = info_n_a
            if 'ИНН' and 'КПП' in tds_all[0].text:
                try:
                    inn = tds_all[-1].text.split(' ')[0]
                    kpp = tds_all[-1].text.split(' ')[-1]
                except:
                    inn = info_n_a
                    kpp = info_n_a
            if 'Дата регистрации' in tds_all[0].text:
                try:
                    registration_date = tds_all[-1].text.split(' ')[0]
                except:
                    registration_date = info_n_a
            if 'Статус' in tds_all[0].text:
                try:
                    status = tds_all[-1].text
                except:
                    status = info_n_a
    else:
        head = info_n_a
        registration_date = info_n_a
        status = info_n_a
        inn = info_n_a
        kpp = info_n_a
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
