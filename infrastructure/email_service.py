import smtplib, ssl
from domain.entities.product import Product 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService():
    def __init__(self, smtp_server, port, password):
        self.smtp_server = smtp_server
        self.port = port
        self.password = password
        self.email_body_template = """Estimado/a [Nombre del destinatario],

            Le informamos de un incidente de seguridad relacionado con uno de nuestros productos, que sospechamos ha sido robado. A continuacion, encontrara los detalles del producto en cuestion:

            Detalles del Producto:
            - Nombre: {name}
            - Color: {color}
            - GTIN: {gtin}
            - Categoria: {categoria}
            - Codigo SKU: {sku_code}
            - Descripcion: {department}
            - Fabric: {fabric}

            Este producto ha sido identificado como potencialmente robado. Si tiene alguna informacion que pueda ayudar en su localizacion, le agradeceriamos que se pusiera en contacto con nosotros de inmediato.

            La seguridad de nuestros productos es una prioridad para nosotros y valoramos cualquier informacion que pueda proporcionar.

            Atentamente,
            [Su Nombre]
            [Nombre de su Empresa]
            [Informacion de Contacto]"""

    def get_email_body(self, product: Product):
        return self.email_body_template.format(name=product.name,
        color=product.color,
        gtin=product.gtin,
        categoria=product.category,
        sku_code=product.sku_code,
        department=product.department,
        fabric=product.fabric)

    def send_email(self, sender, recipient, subject, body):
        try:
            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(sender, self.password)
                server.sendmail(sender, recipient, message.as_string())
                print("Email sent successfully")  # Confirmation message
        except Exception as e:
            print(f"Failed to send email: {e}")  # Error message
