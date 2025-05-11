from database.requests.req_categories import ReqCategory
from pages.dashboard.content.categories.add_category_button import AddCategoryButton
from pages.dashboard.content.categories.category_rows import el_category_header, CategoryRow
from pages.dashboard.head_elements import header
from pages.config.style import inputBgErrorColor
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

        self.column_with_category_rows = ft.Column(
            controls=[],
            spacing=1,
            # height=600,     #scroll не будет работать, если изменить размер окна
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.content_header = header(label_name="Список Категорий", user_role=self.user_role)
        self.new_content.append(self.content_header)

        # resul append to body_content
        req = ReqCategory()
        max_length_category = req.get_max_length()
        name_width = max(max_length_category * 8, 100)  # 7 letter size
        d_width = {"c_edit": 80,
                   "c_category": name_width,
                   "c_cnt": 150,
                   "c_order_sort": 90}


        # кнопка "Добавить новую категорию"
        self.new_content.append(
            AddCategoryButton(page=self.page,
                              d_width=d_width,
                              error_message=error_message,
                              column_with_rows=self.column_with_category_rows,
                              # передается ссылка на список строк, чтобы к нему добавить новую категорию
                              ).build()
        )

        self.new_content.append(el_category_header(d_width))  # table header
        # ---rows---
        for id, c_name, c_order, p_cnt in req.category_products_cnt():
            self.column_with_category_rows.controls.append(
                CategoryRow(
                    page=self.page,
                    d_width=d_width,
                    error_message=error_message,
                    id=id,
                    p_name=c_name,
                    p_product_cnt=str(p_cnt),
                    p_order=c_order,
                    column_with_rows=self.column_with_category_rows,
                )
            )

        self.new_content.append(self.column_with_category_rows)
        # --rows-----------

        self.new_content.append(error_message)

        return self.new_content