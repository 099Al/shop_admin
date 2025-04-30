from database.requests.req_categories import ReqCategory
from pages.dashboard.elements.category_elements import AddCategoryButton, el_category_header, CategoryRow
from pages.dashboard.head_elements import header
from pages.style.style import inputBgErrorColor
import flet as ft



class CategoriesContent:

    def __init__(self, instance):
        #self.instance = instance
        self.page = instance.page
        self.user_role = instance.user_role
        #self.content_header = instance.content_header
        self.new_content = []

    def build(self):
        error_message = ft.SnackBar(
            content=ft.Text('Категория с таким названием уже существует'),
            bgcolor=inputBgErrorColor
        )


        self.content_header = header(label_name="Список Категорий", user_role=self.user_role)
        self.new_content.append(self.content_header)

        # resul append to body_content
        req = ReqCategory()
        max_length_category = req.get_max_length()
        name_width = max(max_length_category * 8, 100)  # 7 letter size
        d_width = {"c1": 80, "c2": name_width, "c3": 150, "c4": 90}

        l_controls = []

        # кнопка "Добавить новую категорию"
        self.new_content.append(
            AddCategoryButton(page=self.page,
                              d_width=d_width,
                              error_message=error_message,
                              l_elements=l_controls,
                              # передается ссылка на список строк, чтобы к нему добавить новую категорию
                              ).build()
        )

        self.new_content.append(el_category_header(d_width))  # table header
        # ---rows---
        for id, c_name, c_order, p_cnt in req.category_products_cnt():
            l_controls.append(CategoryRow(page=self.page,
                                          d_width=d_width,
                                          error_message=error_message,
                                          id=id,
                                          p_name=c_name,
                                          p_product_cnt=str(p_cnt),
                                          p_order=c_order,
                                          l_elements=l_controls,
                                          )
                              )
        self.new_content.append(ft.Column(
            controls=l_controls,
            spacing=1,
            # height=600,     #scroll не будет работать, если изменить размер окна
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ))
        # --rows-----------

        self.new_content.append(error_message)

        return self.new_content