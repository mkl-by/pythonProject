# # This is a sample Python script.

import requests, lxml, re, json
from bs4 import BeautifulSoup

url = 'https://www.mebelshara.ru/contacts'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
           'october_session': 'eyJpdiI6IlJKdThHRXRyd2lta05TQUZTY2hxNnc9PSIsInZhbHVlIjoiSFV1cEtXR3E3RlFhVHJNRFByXC9sQzl4ZTVuRUE1Vmxqelo0MVIrU1wvR1NtVGlXNkRiZ0FHQ3JCXC9iUDV5WjFlb3hYWUZLZEk2c0d1ZFNQOGNSd0VMWTk2U3pyU05CSFk3UWRLejlITXY2b3Y0M2trRVA1WUpNMFA2TEVsYTl0NUgiLCJtYWMiOiI0NDllZDY3MzVhZjUxY2ZmYTBlNDdmMzUwMzJiMzI5ZmE4MzA2Y2Q5MDE1ZjlhMTdkNzNjM2U4MTBhZDA2NTk0In0%3D',
            'cto_bundle': 'BORWP18xUyUyQnFKdVNEUnhLSiUyRk4lMkJPeWxUV04yUHJaMHR3cVUyNzhZT1djNzc2dXRKVDF5czU2OVRGUDRwT09VMU9YOFdnNlltcktKcmRGVSUyRlNLV0VmYXl0UXd4cDVEUkNpY0UlMkZRTmRpTGZ5WEg3RzlWdnU2SWwzZno4RjU3bGluYyUyRkxMb0pOJTJCbkIwbUpOWXdXRXY4ckM1bjF3ZyUzRCUzRA'}

response = requests.get(url, headers=headers)
result = []
# поиск внутри ковычек data-shop-name имя магазина, latitude, longitude - координаты, data-shop-mode1,2 - даты работы
sname = re.compile(r'(?<=data-shop-name=").*?(?=")')
latl1 = re.compile(r'(?<=data-shop-latitude=").*?(?=")')
latl2 = re.compile(r'(?<=data-shop-longitude=").*?(?=")')
data1 = re.compile(r'(?<=data-shop-mode1=").*?(?=")')
data2 = re.compile(r'(?<=data-shop-mode2=").*?(?=")')

soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='city-item')

for n, i in enumerate(items, start=1):
    itemName = i.find('h4', class_='js-city-name').text.strip()
    adress = i.find_all('div', class_='shop-address')
    phoness = i.find_all('div', class_='shop-phone')
    shop_list = i.find_all('div', class_='shop-list-item')

    for nn in range(len(adress)):
        latl = []
        phone = []
        time = []
        datas = []
        # город с адресом
        adr = f'{itemName}, {adress[nn].text.strip()}'
        # телефон
        phone.append(phoness[nn].text.strip())
        # имя магазина с помощью регулярки
        shop_name = f'{sname.findall(str(shop_list))[nn]}'
        # координаты с помощью регулярки
        latl.append(latl1.findall(str(shop_list))[nn])
        latl.append(latl2.findall(str(shop_list))[nn])
        # даты с помощью регулярки
        dd = data1.findall(str(shop_list))[nn]
        if 'Без выходных' in dd:
            datas.append(f'пн-вс: {data2.findall(str(shop_list))[nn]}')
        else:
            datas.append(data1.findall(str(shop_list))[nn])
            datas.append(data2.findall(str(shop_list))[nn])

        result.append({"address": adr, "latlon": latl, "name": shop_name, "phones": phone, "working_hours": datas})

if result:
    with open("file_result.json", "w") as write_file:
        json.dump(result, write_file)

#
# for i in result:
#     print(i)

# json_string = json.dumps(result)
# print(json_string)
