import requests

class APIClient:
    BASE_URL = 'https://api.clientdomain.com/'

    def get_product_info(self, rfid_tag):
        response = requests.get(f"{self.BASE_URL}/products/{rfid_tag}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
