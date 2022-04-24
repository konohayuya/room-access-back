import re
from typing import List, Dict
import requests
import bs4


def bus_to_nagao():
    to_nagao_url = ("http://busnavi.keihanbus.jp/mobile/index.php/Route/TimeSheet"
                    "?key_start=%96k%8ER&key_end=%92%B7%94%F6"
                    "&start=%96k%8ER%92%86%89%9B%81%5E%8B%9E%8D%E3%83o%83X"
                    "&end=%92%B7%94%F6%89w%81%5E%8B%9E%8D%E3%83o%83X"
                    "&se=51c16147635443d9d7c7b4cc04052c33")

    return __keihan_bus_scraping(to_nagao_url)


def bus_to_kuzuha():
    to_kuzuha_url = ("http://busnavi.keihanbus.jp/mobile/index.php/Route/TimeSheet?"
                     "key_start=%96k%8ER&key_end=%8F%BE%97t"
                     "&start=%96k%8ER%92%86%89%9B%81%5E%8B%9E%8D%E3%83o%83X"
                     "&end=%8F%BE%97t%89w%81%5E%8B%9E%8D%E3%83o%83X"
                     "&se=078d638ff4676402c56bb7e7a138e4c6")

    return __keihan_bus_scraping(to_kuzuha_url)


def bus_to_hirakatashi_kita():
    to_hirakatashi_kita_url = ("http://busnavi.keihanbus.jp/mobile/index.php/Route/TimeSheet?"
                               "key_start=%96k%8ER&key_end=%96%87%95%FB%8Es"
                               "&start=%96k%8ER%92%86%89%9B%81%5E%8B%9E%8D%E3%83o%83X"
                               "&end=%96%87%95%FB%8Es%89w%96k%8C%FB%81%5E%8B%9E%8D%E3%83o%83X"
                               "&se=0a2b1e8332021a7b66d318b51a0d37dd")

    return __keihan_bus_scraping(to_hirakatashi_kita_url)


def __keihan_bus_scraping(url: str) -> List[Dict[str, str]]:
    res = requests.get(url, allow_redirects=True)
    if not res.ok:
        return []

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    elem_list: List[bs4.element.Tag] = soup.select('#datalist td')
    if len(elem_list) == 0:
        return []

    delay_replace_r = re.compile('<.+>')

    data_list = [{"time": it[0], "type": delay_replace_r.sub('', it[1])[1:-1]} for it in
                 [tag.get_text().split('\n')[0].replace('\xa0', ' ').split(' ') for tag in elem_list]]

    return data_list
