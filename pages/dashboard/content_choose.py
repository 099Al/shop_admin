import flet as ft

from database.connect import DataBase
from database.requests.req_admins import ReqAdmins
from pages.dashboard.content.admins.admins import AdminsContent
from pages.dashboard.content.categories.categories import CategoriesContent
from pages.dashboard.content.clients.clients import ClientsContent
from pages.dashboard.content.orders.orders import OrdersContent
from pages.dashboard.content.products.products import ProductsContent
from pages.dashboard.content.products_categories.product_categories import ProductsAndCategoriesContent

#from pages.dashboard.content.categories import set_CategoriesContent
from pages.dashboard.head_elements import header
from pages.dashboard.types import EnumDashContent
from pages.config.style import *


class Dash_Content:

    def __init__(self, page, container_data: ft.Container, user_role):
        self.page = page
        self.container_data = container_data
        self.user_role = user_role
        self.content_header = header(label_name="Панель управления", user_role=user_role)
        #print('init', self.content_header.content)
        #self.body_content = [self.content_header]

        self.container_data.content = ft.Column(controls=[self.content_header])




    def update_content(self, content_type):
        match content_type:

            case EnumDashContent.CATEGORY:
                category_content = CategoriesContent(self)
                new_content = category_content.build()
                self.container_data.content = ft.Column(controls=new_content)


            case EnumDashContent.PRODUCTS:
                product_content = ProductsContent(self)
                new_content = product_content.build()
                self.container_data.content = ft.Column(controls=new_content)

            case EnumDashContent.PRODUCTS_AND_CATEGORIES:
                product_categories_content = ProductsAndCategoriesContent(self)
                content = product_categories_content.build()
                self.container_data.content = ft.Column(controls=content)

            case EnumDashContent.ADMINS:
                admins_content = AdminsContent(self)
                content = admins_content.build()
                self.container_data.content = ft.Column(controls=content)

            case EnumDashContent.CLIENTS:
                clients_content = ClientsContent(self)
                content = clients_content.build()
                self.container_data.content = ft.Column(controls=content)

            case EnumDashContent.ORDERS:
                order_content = OrdersContent(self)
                content = order_content.build()
                self.container_data.content = ft.Column(controls=content)


        self.page.update()


