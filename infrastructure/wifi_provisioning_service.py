# infrastructure/wifi_provisioning_service.py
import subprocess
import os

class WiFiProvisioningService:
    WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"

    @staticmethod
    def start_access_point():
        try:
            # Comandos para iniciar el punto de acceso
            # Por ejemplo, iniciar hostapd y dnsmasq
            subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'], check=True)
            subprocess.run(['sudo', 'systemctl', 'start', 'dnsmasq'], check=True)
        except Exception as e:
            print(f"Error al iniciar el punto de acceso: {e}")

    @staticmethod
    def stop_access_point():
        try:
            # Comandos para detener el punto de acceso
            subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'], check=True)
            subprocess.run(['sudo', 'systemctl', 'stop', 'dnsmasq'], check=True)
        except Exception as e:
            print(f"Error al detener el punto de acceso: {e}")

    @staticmethod
    def setup_wifi(ssid: str, password: str):
        try:
            # Añadir la configuración de WiFi al archivo wpa_supplicant.conf
            with open(WiFiProvisioningService.WPA_SUPPLICANT_CONF, 'a') as file:
                file.write(
                    f'\nnetwork={{\n'
                    f'    ssid="{ssid}"\n'
                    f'    psk="{password}"\n'
                    f'    key_mgmt=WPA-PSK\n}}\n'
                )
            # Recargar la configuración de wpa_supplicant
            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'], check=True)
            return True
        except Exception as e:
            print(f"Error al configurar WiFi: {e}")
            return False

    @staticmethod
    def is_wifi_connected():
        try:
            # Comprobar si hay una conexión WiFi activa
            result = subprocess.run(['iwgetid'], capture_output=True, text=True)
            return not ('ESSID:""' in result.stdout or result.stdout == '')
        except Exception as e:
            print(f"Error al verificar la conexión WiFi: {e}")
            return False

    @staticmethod
    def list_available_networks():
        try:
            scan_output = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan'])
            networks = WiFiProvisioningService.parse_networks(scan_output.decode('utf-8'))
            return networks
        except subprocess.CalledProcessError as e:
            print(f"Error scanning for networks: {e}")
            return []

    @staticmethod
    def parse_networks(scan_output):
        networks = []
        for line in scan_output.split('\n'):
            if "ESSID" in line:
                ssid = line.split(':')[1].strip().strip('"')
                networks.append(ssid)
        return networks