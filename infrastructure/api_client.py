import requests
from domain.entities.product import Product

class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

    def get_product_info(self, gtin: str) -> dict:
        response = requests.get(f"{self.base_url}/retrieve_by_gtin?gtins[]={gtin}", headers=self.headers)
        if response.status_code == 200:
            product_data = response.json()[0]
            return Product(**product_data)
        else:
            return None
