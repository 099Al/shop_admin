import flet as ft

from database.connect import DataBase
from database.requests.req_admins import ReqAdmins
from database.requests.req_products import ReqCategory
from pages.dashboard.elements.admin_elements import AdminRow, AdminHeader
from pages.dashboard.elements.category_elements import el_category_header, CategoryRow, AddCategoryButton  # el_add_category
from pages.dashboard.elements.row_width import RowWidth_Admin
from pages.dashboard.head_elements import header
from pages.dashboard.types import EnumDashContent
from pages.style.style import *


class Dash_Content():

    def __init__(self, page, user_role):
        self.page = page
        self.user_role = user_role
        self.content_header = header(label_name="Панель управления", user_role=user_role)
        self.body_content = [self.content_header]



    def update_content(self, content_type):
        match content_type:
            case EnumDashContent.CATEGORY:

                error_message = ft.SnackBar(
                    content=ft.Text('Категория с таким названием уже существует'),
                    bgcolor=inputBgErrorColor
                )

                self.body_content.clear()
                self.content_header = header(label_name="Список Категорий", user_role=self.user_role)
                self.body_content.append(self.content_header)


                # resul append to body_content
                db = DataBase()
                req = ReqCategory(db)
                max_length_category = req.get_max_length()
                name_width = max(max_length_category * 8, 100)  # 7 letter size

                l_controls = []

                #кнопка "Добавить новую категорию"
                self.body_content.append(
                    AddCategoryButton(page=self.page,
                                      name_width=name_width,
                                      error_message=error_message,
                                      l_elements=l_controls,    #передается ссылка на список строк, чтобы к нему добавить новую категорию
                                      )
                )

                self.body_content.append(el_category_header(name_width))  # table header
                #---rows---
                for id, c_name, p_cnt in req.category_products_cnt():
                    l_controls.append(CategoryRow(page=self.page,
                                                  name_width=name_width,
                                                  error_message=error_message,
                                                  id=id,
                                                  p_name=c_name,
                                                  p_product_cnt=str(p_cnt),
                                                  l_elements=l_controls,
                                                  )
                                      )
                self.body_content.append(ft.Column(
                    controls=l_controls,
                    spacing=1,
                    #height=600,     #scroll не будет работать, если изменить размер окна
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                ))
                #--rows-----------

                self.body_content.append(error_message)



            case EnumDashContent.PRODUCTS:
                error_message_product = ft.SnackBar(
                    content=ft.Text(''),
                    bgcolor=inputBgErrorColor
                )

                self.body_content.clear()
                self.body_content.append(self.content_header)






            case EnumDashContent.ADMINS:
                error_message_user = ft.SnackBar(
                    content=ft.Text(''),
                    bgcolor=inputBgErrorColor
                )
                self.body_content.clear()
                self.content_header = header(label_name="Список Пользователей", user_role=self.user_role)
                self.body_content.append(self.content_header)

                db = DataBase()
                req = ReqAdmins(db)
                #max_length_category = req.get_max_length()
                #name_width = max(max_length_category * 8, 100)  # 7 letter size

                l_controls = []

                # self.body_content.append(
                #     AddAdminButton(page=self.page,
                #                       name_width=name_width,
                #                       error_message=error_message,
                #                       l_elements=l_controls,
                #                       )
                # )

                letter_width = 9

                header_admin = AdminHeader(letter_width)
                self.body_content.append(header_admin)  # table header

                d_width = header_admin.header_size()
                # ---rows--- telegram_id, telegram_name, role, name, phone, email, login,


                for admin in req.get_all_users():
                    d_width["telegram_id"] = max(d_width["telegram_id"], len(str(admin.telegram_id))*letter_width)
                    d_width["role"] = max(d_width["role"], 1 if admin.role is None else len(admin.role)*letter_width)
                    d_width["name"] = max(d_width["name"], 1 if admin.name is None else len(admin.name)*letter_width)
                    d_width["phone"] = max(d_width["phone"], 1 if admin.phone is None else len(admin.phone)*letter_width)
                    d_width["email"] = max(d_width["email"], 1 if admin.email is None else len(admin.email)*letter_width)
                    d_width["login"] = max(d_width["login"], 1 if admin.login is None else len(admin.login)*letter_width)
                    l_controls.append(AdminRow(page=self.page,
                                                  #error_message=error_message,
                                                  telegram_id=str(admin.telegram_id),
                                                  role=admin.role,
                                                  phone=admin.phone,
                                                  name=admin.name,
                                                  email=admin.email,
                                                  login=admin.login,
                                                  l_elements=l_controls,
                                                  d_width=d_width
                                               )
                                      )
                #set width for header
                header_admin.resize(d_width)

                #set width for row
                for row in l_controls:
                    if isinstance(row, AdminRow):
                        row.resize(d_width)

                self.body_content.append(ft.Column(
                    controls=l_controls,
                    spacing=1,
                    # height=600,     #scroll не будет работать, если изменить размер окна
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                ))


                self.body_content.append(ft.Text("CONTENT3"))
            case _:
                self.body_content.append(ft.Text("CONTENT"))

        self.page.update()


