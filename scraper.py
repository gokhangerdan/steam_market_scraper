import requests
from datetime import datetime
import pandas as pd
import time


cookies = {
    'timezoneOffset': '10800,0',
    '_ga': 'GA1.2.1635737524.1534347633',
    '_gid': 'GA1.2.1013207254.1534679427',
    'sessionid': 'eb12d25cbe457c6d8bf930be',
    'steamCountry': 'TR%7C5aef4de0d602c1d4800242dfaf8a3ec6',
    'Steam_Language': 'english',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'Referer': 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_ak47&category_730_Quality%5B%5D=tag_normal&appid=730',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'X-Prototype-Version': '1.7',
}

params = (
    ('query', ''),
    ('start', '0'),
    ('count', '100'),
    ('search_descriptions', '0'),
    ('sort_column', 'price'),
    ('sort_dir', 'desc'),
    ('appid', '730'),
    ('category_730_ItemSet[]', 'any'),
    ('category_730_ProPlayer[]', 'any'),
    ('category_730_StickerCapsule[]', 'any'),
    ('category_730_TournamentTeam[]', 'any'),
    ('category_730_Weapon[]', 'tag_weapon_ak47'),
    ('category_730_Quality[]', 'tag_normal'),
)

response = requests.get('https://steamcommunity.com/market/search/render/', headers=headers, params=params, cookies=cookies)

t = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")

s = response.text

image_link = []
weapon = []
name = []
exterior = []
currency = []
sale_price = []
dt = []
for i in range(s.count("currency")):
    f = s.find('img id')
    s = s[f:]
    f = s.find('src')
    s = s[f+6:]
    f = s.find('" ')
    img = s[:f]
    image_link.append(s)
    f = s.find('data-currency')
    s = s[f+21:]
    f = s.find(' USD')
    price_buy = s[:f]
    currency.append(price_buy)
    f = s.find('sale_price')
    s = s[f + 14:]
    f = s.find(' USD')
    price_sale = s[:f]
    sale_price.append(price_sale)
    f = s.find(';\\">')
    s = s[f + 4:]
    weapon.append(s[:s.find(' | ')])
    name.append(s[s.find(' | ') + 3:s.find(' (')])
    exterior.append(s[s.find(' (') + 2:s.find(')')])
    dt.append(t)

df = pd.DataFrame({"weapon": weapon,
                   "name": name,
                   "exterior": exterior,
                   "currency": currency,
                   "sale_price": sale_price,
                   "dt": dt})

mylist = df.to_dict("records")
print(mylist)
