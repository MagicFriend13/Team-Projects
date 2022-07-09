# https://www.youtube.com/watch?v=n7BIbh_-WG4&t=357s

from bs4 import BeautifulSoup
import requests

# url = "https://120w.ru/zaryadnoe_ustroystvo/Acer/"
# item = (BeautifulSoup(requests.get(url).text, "html.parser").find("li", class_="bx-pag-prev")).get('href')

# print(item)

# while (BeautifulSoup(requests.get(url).text, "html.parser").find("li", class_="bx-pag-prev")).get('href') is not None:
item_properties = []

url = "https://120w.ru"
#t3_link = "https://120w.ru/vse-zaryadki/hp_2/originalnyy_akkumulyator_dlya_hp_nsi_8060_o_73_wh_14_4v/"
#t3_link = "https://120w.ru/vse-zaryadki/acer/originalnyy_blok_pitaniya_dlya_acer_19v_3_42a_5_5_1_7_65w/"
t3_link = "https://120w.ru/aksessuary/originalnyy_adapter_pitaniya_dlya_apple_5v_2_4a_lightning_12w/"
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
        img_name = var[-7:]

        with open(f"images/{img_name}", "wb") as f:
            f.write(img.content)

        item_properties.append(str(img_name))
    else:
        item_properties.append("No Image")

if len(item_properties) < 30:
    for i in range(30-len(item_properties)):
        item_properties.append('')

with open('main.csv', "a+") as main_table:
    x = 0
    for element in item_properties:
        element = f'"{element}"'
        print(item_properties[-1])
        print(element)
        if x != 29:
            element += ','
        else:
            element += '\r'
        main_table.write(element)
        x += 1
