# In the application layer
from infrastructure.wifi_provisioning_service import WiFiProvisioningService

class ProvisioningApplicationService:
    @staticmethod
    def provision_device(ssid: str, password: str):
        if WiFiProvisioningService.setup_wifi(ssid, password):
            print("WiFi provisioning successful.")
        else:
            print("WiFi provisioning failed.")
