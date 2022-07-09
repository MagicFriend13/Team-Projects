import requests
from bs4 import BeautifulSoup


url = "https://120w.ru"

sublynks_array = []
sublynks_array_t2 = []
sublynks_array_t3 = []
result = []

request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")
item = soup.find_all("li", class_="bx-nav-1-lvl bx-nav-list-0-col")
item += soup.find_all("li", class_="bx-nav-1-lvl bx-nav-list-0-col bx-active")

for items in item:
    sublynks_array.append(url + str((items.find("a")).get('href')))

for sublynk in sublynks_array:

    request = requests.get(sublynk)
    soup = BeautifulSoup(request.text, "html.parser")

    item = soup.find_all("a", class_="bx_catalog_tile_img")
    for items in item:
        sublynks_array_t2.append(url + str(items.get('href')))

    item = soup.find_all("a", class_="bx_catalog_item_images")
    for items in item:
        sublynks_array_t3.append(url + str(items.get('href')))
print('End of part 1')

for sublynk in sublynks_array_t2:

    x = 0
    nex = ''

    while True:

        if x == 0:
            link = sublynk
        else:
            link = url + nex

        request = requests.get(link)
        soup = BeautifulSoup(request.text, "html.parser")

        item = soup.find_all("a", class_="bx_catalog_item_images")
        for items in item:
            sublynks_array_t3.append(url + str(items.get('href')))

        try:
            nex = soup.find(class_="bx-pag-next").find("a").get("href")
        except AttributeError:
            break
        x += 1

print('End of part 2')

counter_for_img_name = 0

for t3_link in sublynks_array_t3:

    item_properties = []

    request = requests.get(t3_link)
    soup = BeautifulSoup(request.text, "html.parser")

    item = soup.find("span", class_="bx_bigimages_aligner").find("img").get("title")
    item_properties.append(str(item))

    item = soup.find_all("td", class_="myTd")
    for items in item:
        item_properties.append(str(items.text))

    item = soup.find(class_="item_current_price")

    item_properties.append("Цена")
    item_properties.append(str(item.text))

    item = soup.find_all(class_="cnt_item")

    for items in item:

        var = str(items["style"])[22:-3]

        if var != "/bitrix/templates/new/components/bitrix/catalog.element/prop_sort/images/no_photo.png":

            img_url = url + var
            img = requests.get(img_url)
            img_name = str(counter_for_img_name) + var[-3:]

            with open(f"images/{img_name}", "wb") as f:
                f.write(img.content)

            item_properties.append(str(img_name))
        else:
            item_properties.append("No Image")

    if len(item_properties) < 30:
        for i in range(30 - len(item_properties)):
            item_properties.append('')

    with open('main.csv', "a+") as main_table:
        x = 0
        for element in item_properties:
            element = f'"{element}"'

            if x != 29:
                element += ','
            else:
                element += '\r'
            main_table.write(element)
            x += 1
    counter_for_img_name += 1

print('End of part 3')
