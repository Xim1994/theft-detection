# application/services/provisioning_application_service.py
from infrastructure.wifi_provisioning_service import WiFiProvisioningService
from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)
networks = []

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    global networks 

    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        if ProvisioningApplicationService.provision_wifi(ssid, password):
            WiFiProvisioningService.stop_access_point()  # Opcional: detener el AP después de configurar
            return "WiFi configurado exitosamente. Por favor, reinicie el dispositivo."
        else:
            return "Falló la configuración de WiFi."
    return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>Detección de Robos - Configuración WiFi</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h2 { color: #333; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; }
                input[type="text"], input[type="password"] { width: 100%; padding: 8px; }
                button { padding: 10px 15px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <h2>Detección de Robos - Configuración WiFi</h2>
            <form method="post">
                <div class="form-group">
                    <label for="ssid">SSID:</label>
                    <select name="ssid">
                        {% for network in networks %}
                            <option value="{{ network }}">{{ network }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" name="password">
                </div>
                <button type="submit">Configurar WiFi</button>
            </form>
        </body>
        </html>
    ''', networks=networks)

class ProvisioningApplicationService:
    @staticmethod
    def provision_wifi(ssid: str, password: str):
        return WiFiProvisioningService.setup_wifi(ssid, password)

    @staticmethod
    def check_and_start_ap():
        global networks 

        if not WiFiProvisioningService.is_wifi_connected():
            networks = WiFiProvisioningService.list_available_networks()
            WiFiProvisioningService.start_access_point()
            # Iniciar el servidor web Flask en modo de punto de acceso
            app.run(host='0.0.0.0', port=80)
