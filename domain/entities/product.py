class Product:
    def __init__(self, gtin, barcodes, code, brand, season, name, option, style, color, sizes, category, prices, department, fabric, sku_code, option_code, refill_category, image_url, last_updated, gs1_company_prefix_length):
        self.gtin = gtin
        self.barcodes = barcodes  # This can be a list of Barcode objects
        self.code = code
        self.brand = brand
        self.season = season
        self.name = name
        self.option = option
        self.style = style
        self.color = color
        self.sizes = sizes  # This can be a list of Size objects
        self.category = category
        self.prices = prices  # This can be a list of Price objects
        self.department = department
        self.fabric = fabric
        self.sku_code = sku_code
        self.option_code = option_code
        self.refill_category = refill_category
        self.image_url = image_url
        self.last_updated = last_updated
        self.gs1_company_prefix_length = gs1_company_prefix_length

    # You can add methods that represent behaviors or business logic related to a product
