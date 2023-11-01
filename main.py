import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime as dt
import time
import csv
import regex as re
from lxml import etree
import html
import os
from datetime import timedelta

from sqlalchemy.util.topological import sort

url = 'https://remoteok.com/'
HOST = 'https://remoteok.com'

os.path.dirname("Vacations")
if not os.path.exists("Vacations"):
    os.makedirs("Vacations")
folder_path = 'C:\\Users\DELL\PycharmProjects\Trainii\Topizdato\Remoteok Day\\Vacations'
file_names = []
for entry in os.scandir(folder_path):
    if entry.is_file():
        file_names.append(entry.name)
time_now = str(datetime.datetime.now())
file_time1 = str(time_now.split('.')[:1])
file_time = file_time1.replace('[', '').replace(']', '')  # .replace(''', '')
file_name1 = dt.strptime(file_time, "'%Y-%d-%m %H:%M:%S'")
file_name = str(file_name1).replace(':', '.')

time_ranges = []
for i in file_names:
    clean_name1 = i.replace('.csv', '')
    clean_name = dt.strptime(clean_name1, '%Y-%d-%m %H.%M.%S')

    time_now = datetime.datetime.now()
    time_range1 = time_now - clean_name
    time_range = time_range1.total_seconds()/60
    time_ranges.append(time_range)
last_report = min(time_ranges)

for i in range(0,500, 20):
    url2 = f'https://remoteok.com/?&action=get_jobs&offset={i}'
    data2 = {
        'authority': 'remoteok.com',
        'method': 'GET',
        'path': f'/?&action=get_jobs&offset={i}',
        'scheme': 'https',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'ref=https%3A%2F%2Fwww.google.com%2F; new_user=false; cf_clearance=sbfm.ApPOqyh9GMeBZsd2ct57SIq_Tgh_I1U7T8QwjU-1696583544-0-1-4dc2ac5.2e45a725.53dd7525-250.0.0; logged_in_token=reyter_a8fce7b9b82a6596036a25637a0d0182; PHPSESSID=hqbpmqdcc4ujcespri5pcbmi1d; visit_count=9; visits=18; adShuffler=0',
        'Referer': 'https://remoteok.com/',
        'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest`'
        }

    if data2:
        r = requests.get(url2, headers=data2)
        soup = BeautifulSoup(r.content, 'lxml')
        all_blocks = soup.select('[class~=job]')#[:1]
        # print(all_blocks)
        for i in all_blocks:
            post_days1 = i.find('td', class_='time')#.text
            post_days2 = post_days1.select('[datetime]')#.split()#[0]
            post_days3 = str(post_days2).split('"')[1].split('T')
            post_days4 = str(post_days3).split('+')[0:1]

            for item in post_days4:
                date1 = item.replace("'", '').replace(',', '').replace('[', '')
                time_note = dt.strptime(date1, "%Y-%m-%d %H:%M:%S")
                time_now = datetime.datetime.now()
                time_range1 = time_now-time_note
                time_range = time_range1.total_seconds() / 60
                if time_range < last_report:
                    title2 = i.find(attrs={'itemprop': 'title'})#[:1]
                    if title2:
                        title = title2.text.strip()
                    else:
                        pass
                    company2 = i.find(attrs={'itemprop': 'name'})
                    if company2:
                        company = company2.text.strip()
                    else:
                        pass
                    salary2 = i.find_all('div', class_='location')  # [1]
                    for a in salary2:
                        if a and re.search(r'💰|đ°', str(a)):
                            salary1 = str(a.text)#.strip()
                            salary = re.sub("[^$-A-Za-z0-9]", " ", salary1)
                        else:
                            pass
                    direction2 = i.find_all('h3')[1:]
                    direction = []
                    for b in direction2:
                        direction1 = b.text.strip()
                        direction.append(direction1)
                    if i:
                        location2 = i.find_all('div', class_='location')[:-1]
                        location3 = str(location2).replace('[]', '')  # .strip()
                        g = location3.rfind('💰')
                        if g != -1:
                            location3 = location3[:g]
                        soup3 = BeautifulSoup(location3, 'html.parser')
                        location4 = str(soup3.text)
                        # s1 = "".join(c for c in location4 if c.isalnum())
                        location = re.sub("[^A-Za-z]", " ", location4).strip()
                    else:
                        pass
                    vacation_url1 = i.find_all(attrs={'itemprop':"url"})
                    for d in vacation_url1:
                        vacation_url = HOST + d.get('href')
                    post_days2 = i.find('td', class_='time')#.text
                    if post_days2:
                        post_days = post_days2.text.strip()
                    else:
                        pass

                    all_data = {'Title2': title,
                                'Company': company,
                                'Salary': salary,
                                'Direction': direction,
                                'Location': location,
                                'URL': vacation_url,
                                'Post days': post_days}


                    # file_name = f'{file_time}.csv'.replace('[', '').replace(']', '')
                    with open(f'Vacations/{file_name}.csv', 'a', encoding="utf-8") as f:
                        w = csv.DictWriter(f, all_data.keys())
                        if f.tell() == 0:
                            w.writeheader()
                        w.writerow(all_data)
                else:
                    pass

    else:
        pass



