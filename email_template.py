email_body = """ Asunto: Alerta de Seguridad - Posible Robo de Producto

Estimado/a [Nombre del destinatario],

Le informamos de un incidente de seguridad relacionado con uno de nuestros productos, que sospechamos ha sido robado. A continuación, encontrará los detalles del producto en cuestión:

Detalles del Producto:
- Nombre: {producto.nombre}
- Color: {producto.color}
- GTIN: {producto.gtin}
- Marca: {producto.marca}
- Categoría: {producto.categoria}
- Código SKU: {producto.sku_code}
- Descripción: {producto.descripcion}

Este producto ha sido identificado como potencialmente robado. Si tiene alguna información que pueda ayudar en su localización, le agradeceríamos que se pusiera en contacto con nosotros de inmediato.

La seguridad de nuestros productos es una prioridad para nosotros y valoramos cualquier información que pueda proporcionar.

Atentamente,
[Su Nombre]
[Nombre de su Empresa]
[Información de Contacto]"""