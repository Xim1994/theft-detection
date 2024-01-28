from application.services.provisioning_application_service import ProvisioningApplicationService
from infrastructure.wifi_provisioning_service import WiFiProvisioningService
from application.handlers.detection_handler import DetectionHandler

if __name__ == '__main__':
    # Verificar la conexión WiFi y, si es necesario, iniciar el punto de acceso y el servidor Flask
    ProvisioningApplicationService.check_and_start_ap()

    # Si ya está conectado a WiFi, continuar con el flujo normal de la aplicación
    if WiFiProvisioningService.is_wifi_connected():
        detection_handler = DetectionHandler()

    # Main loop
    while True:
        detection_handler.handle_detection()
