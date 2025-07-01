import requests
import json
from typing import List, Dict


BASE_URL = 'https://search.wb.ru/exactmatch/sng/common/v13/search'

HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.google.com/",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }


class WBParser:
    """Class to parse products from the website wildberries."""

    def __init__(self, query: str,  pages: int = 1):
        """
        :param query: product to parse.
        :param pages: count of pages to parse.
        """
        self.query = query
        self.pages = pages

    @staticmethod
    def extract_products_info(response_data: Dict) -> List[Dict]:
        """
        Converts products from an API response into a convenient list of dictionaries.

        :param response_data: received data from WB.
        """
        products = response_data.get("data", {}).get("products", [])
        result = []

        for product in products:
            sizes = product.get("sizes", [{}])[0]
            price = sizes.get("price", {})

            basic_price = int(price.get('basic'))
            total_price = int(price.get('total'))

            price_basic = basic_price / 100 if isinstance(basic_price, (int, float)) else None
            price_with_discount = total_price / 100 if isinstance(total_price, (int, float)) else None

            result.append({
                'id': product.get('id'),
                'name': product.get('name'),
                'price_basic': price_basic,
                'price_with_discount': price_with_discount,
                'rating': product.get('reviewRating'),
                'feedbacks': product.get('feedbacks'),
            })

        return result

    def get_products(self) -> List[Dict]:
        """
        Gets all products according query and count of pages to parse.
        """
        all_products = []

        for i in range(1, self.pages + 1):
            params = {
                'ab_testing': 'false',
                'appType': '1',
                'curr': 'rub',
                'dest': '-59202',
                'hide_dtype': '10;13;14',
                'lang': 'ru',
                'page': str(i),
                'query': self.query,
                'resultset': 'catalog',
                'sort': 'popular',
                'spp': '30',
                'suppressSpellcheck': 'false'
            }

            try:
                response = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
                response.raise_for_status()
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    # logging
                    print(f'Decoding error JSON for "{self.query}" in page #{i}')
                    continue
            except requests.RequestException as e:
                # logging
                print(f'Error for "{self.query}" in page #{i}: {e}')
                continue

            if response.status_code == 200:
                # logging
                print(f'Parsing for "{self.query}" page: {i}')
                products = self.extract_products_info(data)
                all_products.extend(products)
            else:
                # logging
                print(f'Can not get for "{self.query}" page: {i}')

        return all_products


if __name__ == "__main__":
    parser = WBParser('футболка женская', 3)
    all_products = parser.get_products()
    print(len(all_products))
    for product in all_products:
        print(f'{product.get("name")} = {product.get("price_with_discount")}')
