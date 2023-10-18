# variables for orders app

# Order table fields
ORDER_ADDRESS_ML = 255
ORDER_ARTICLE_ML = 50
ORDER_PHONE_ML = 20
ORDER_STATUS_ML = 50
ORDER_TOTAL_MDIGIT = 10
ORDER_TOTAL_DECIMAL = 2

# Order table fields
ORD_PROD_PRICE_MDIGIT = 10
ORD_PROD_PRICE_DECIMAL = 2

# DeliveryAddress table fields
DEL_ADDR_COUNTRIES = (
    ("RU", "Россия"),
    ("BY", "Белоруссия"),
    ("KZ", "Казахстан"),
    ("UZ", "Узбекистан"),
)

DEL_ADDR_CITY_ML = 50
DEL_ADDR_STREET_ML = 100
DEL_ADDR_HOUSE_ML = 10
DEL_ADDR_APARTMENT_ML = 10

# Making session keys
CART_SESSION_ID = "cart"
ORDER_SESSION_ID = "order_id"
