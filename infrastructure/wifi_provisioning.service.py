import os
import subprocess

class WiFiProvisioningService:
    WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"

    @staticmethod
    def setup_wifi(ssid: str, password: str) -> bool:
        # You would typically also have validations and error handling here.
        config_lines = [
            '\nnetwork={',
            f'    ssid="{ssid}"',
            f'    psk="{password}"',
            '    key_mgmt=WPA-PSK',
            '}\n'
        ]

        try:
            # Backup the original configuration file
            subprocess.run(['sudo', 'cp', WiFiProvisioningService.WPA_SUPPLICANT_CONF,
                            WiFiProvisioningService.WPA_SUPPLICANT_CONF + '.bak'], check=True)

            # Write the new WiFi configuration
            with open(WiFiProvisioningService.WPA_SUPPLICANT_CONF, 'a') as file:
                file.writelines(config_lines)

            # Reconfigure the WiFi interface
            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'], check=True)

            return True
        except Exception as e:
            print(f"An error occurred while setting up WiFi: {e}")
            return False
