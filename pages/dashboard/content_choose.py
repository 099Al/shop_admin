import flet as ft

from database.connect import DataBase
from database.requests.req_admins import ReqAdmins
from pages.dashboard.content.admins.admins import AdminsContent
from pages.dashboard.content.categories.categories import CategoriesContent
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


            #     error_message_user = ft.SnackBar(
            #         content=ft.Text(''),
            #         bgcolor=inputBgErrorColor
            #     )
            #     self.body_content.clear()
            #     self.content_header = header(label_name="Список Пользователей", user_role=self.user_role)
            #     self.body_content.append(self.content_header)
            #
            #     db = DataBase()
            #     req = ReqAdmins(db)
            #     #max_length_category = req.get_max_length()
            #     #name_width = max(max_length_category * 8, 100)  # 7 letter size
            #
            #     l_controls = []
            #
            #     # self.body_content.append(
            #     #     AddAdminButton(page=self.page,
            #     #                       name_width=name_width,
            #     #                       error_message=error_message,
            #     #                       l_elements=l_controls,
            #     #                       )
            #     # )
            #
            #     letter_width = 9
            #
            #     header_admin = AdminHeader(letter_width)
            #     self.body_content.append(header_admin)  # table header
            #
            #     d_width = header_admin.header_size()
            #     # ---rows--- telegram_id, telegram_name, role, name, phone, email, login,
            #
            #
            #     for admin in req.get_all_users():
            #         d_width["telegram_id"] = max(d_width["telegram_id"], len(str(admin.telegram_id))*letter_width)
            #         d_width["role"] = max(d_width["role"], 1 if admin.role is None else len(admin.role)*letter_width)
            #         d_width["name"] = max(d_width["name"], 1 if admin.name is None else len(admin.name)*letter_width)
            #         d_width["phone"] = max(d_width["phone"], 1 if admin.phone is None else len(admin.phone)*letter_width)
            #         d_width["email"] = max(d_width["email"], 1 if admin.email is None else len(admin.email)*letter_width)
            #         d_width["login"] = max(d_width["login"], 1 if admin.login is None else len(admin.login)*letter_width)
            #         l_controls.append(AdminRow(page=self.page,
            #                                       #error_message=error_message,
            #                                       telegram_id=str(admin.telegram_id),
            #                                       role=admin.role,
            #                                       phone=admin.phone,
            #                                       name=admin.name,
            #                                       email=admin.email,
            #                                       login=admin.login,
            #                                       l_elements=l_controls,
            #                                       d_width=d_width
            #                                    )
            #                           )
            #     #set width for header
            #     header_admin.resize(d_width)
            #
            #     #set width for row
            #     for row in l_controls:
            #         if isinstance(row, AdminRow):
            #             row.resize(d_width)
            #
            #     self.body_content.append(ft.Column(
            #         controls=l_controls,
            #         spacing=1,
            #         # height=600,     #scroll не будет работать, если изменить размер окна
            #         scroll=ft.ScrollMode.AUTO,
            #         expand=True
            #     ))
            #
            #
            #     self.body_content.append(ft.Text("CONTENT3"))
            # case _:
            #     self.body_content.append(ft.Text("CONTENT"))

        # self.page.update()
        #self.page.views[0].controls = self.body_content
        self.page.update()


