import copy

import flet as ft

from database.connect import DataBase
from database.requests.req_products import ReqCategory
from pages.dashboard.head_elements import header
from pages.dashboard.types import EnumDashContent
from pages.style.style import *


class Dash_Content():

    def __init__(self, page, user_role):
        self.page = page
        self.content_header = header(user_role)
        self.body_content = [self.content_header]


    def update_content(self, content_type):
        match content_type:
            case EnumDashContent.CATEGORY:
                self.body_content.clear()
                self.body_content.append(self.content_header)
                db = DataBase()
                req = ReqCategory(db)
                l_categories = req.get_all_categories()
                for x in l_categories:
                    self.body_content.append(ft.Text(x.name))
            case EnumDashContent.PRODUCTS:
                self.body_content.clear()
                self.body_content.append(self.content_header)
            case "content3":
                self.body_content.append(ft.Text("CONTENT3"))
            case _:
                self.body_content.append(ft.Text("CONTENT"))

        self.page.update()