import copy

import flet as ft

from database.connect import DataBase
from database.requests.req_products import ReqCategory
from pages.dashboard.category_elements import el_header, CategoryRow
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
                max_length_category = req.get_max_length()


                # resul append to body_content
                name_width = max(max_length_category*8, 100) #7 letter size
                self.body_content.append(el_header(name_width))
                res_categories = req.category__products_cnt()
                l_controls = []
                d_elements = {i:i for i in range(len(res_categories))}
                for k, (id, c_name, p_cnt) in enumerate(req.category__products_cnt()):
                    l_controls.append(CategoryRow(id=id,
                                                  p_name=c_name,
                                                  p_cnt=str(p_cnt),
                                                  name_width=name_width,
                                                  page=self.page,
                                                  controls=l_controls,
                                                  index=k,
                                                  index_of_elements=d_elements
                                                  )
                                      )
                self.body_content.append(ft.Column(
                    controls=l_controls,
                    spacing=1
                ))
                # self.body_content.append(self.el_row())




            case EnumDashContent.PRODUCTS:
                self.body_content.clear()
                self.body_content.append(self.content_header)
            case "content3":
                self.body_content.append(ft.Text("CONTENT3"))
            case _:
                self.body_content.append(ft.Text("CONTENT"))

        self.page.update()