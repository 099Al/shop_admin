from enum import Enum, auto

class EnumDashContent(Enum):
    CATEGORY = auto()
    PRODUCTS = auto()
    PRODUCTS_AND_CATEGORIES = auto()
    ADMINS = auto()
    CLIENTS = auto()
    ORDERS = auto()