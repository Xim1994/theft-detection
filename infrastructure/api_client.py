import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_product_info(self, rfid_tag: str) -> dict:
        response = requests.get(f"{self.base_url}/products/{rfid_tag}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
