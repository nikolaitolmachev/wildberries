import unittest
import requests
import json
from unittest.mock import patch, Mock
from backend.app.parser import WBParser


class TestWBParser(unittest.TestCase):

    def setUp(self):
        self.parser = WBParser('футболка женская', pages=2)

    def test_extract_products_info_valid(self):
        response_data = {
            "data": {
                "products": [
                    {
                        "name": "Product 1",
                        "sizes": [{"price": {"basic": 1000, "total": 800}}],
                        "reviewRating": 4.8,
                        "feedbacks": 555
                    }
                ]
            }
        }
        result = self.parser.extract_products_info(response_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Product 1')
        self.assertEqual(result[0]['price_basic'], 1000)
        self.assertEqual(result[0]['price_with_discount'], 800)
        self.assertEqual(result[0]['rating'], 4.8)
        self.assertEqual(result[0]['feedbacks'], 555)

    def test_extract_products_info_empty(self):
        response_data = {}
        result = self.parser.extract_products_info(response_data)
        self.assertEqual(result, [])

    @patch('backend.app.parser.requests.get')
    def test_get_products_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "products": [
                    {
                        "name": "Product 1",
                        "sizes": [{"price": {"basic": 1000, "total": 800}}],
                        "reviewRating": 4.8,
                        "feedbacks": 555
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        products = self.parser.get_products()
        self.assertTrue(len(products) > 0)
        self.assertEqual(products[0]['name'], 'Product 1')
        self.assertEqual(mock_get.call_count, self.parser.pages)

    @patch('backend.app.parser.requests.get')
    def test_get_products_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException('Network error')

        products = self.parser.get_products()
        self.assertEqual(products, [])

    @patch('backend.app.parser.requests.get')
    def test_get_products_json_decode_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Mock(side_effect=json.JSONDecodeError('Expecting value', '', 0))
        mock_get.return_value = mock_response

        products = self.parser.get_products()
        self.assertEqual(products, [])

    @patch('backend.app.parser.requests.get')
    def test_get_products_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        products = self.parser.get_products()
        self.assertEqual(products, [])


if __name__ == "__main__":
    unittest.main()

