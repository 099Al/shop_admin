from database.requests.req_categories import ReqCategory
from pages.config.errors import error_message_categtory
from pages.config.sizes import d_category_width
from pages.dashboard.content.categories.add_category_button import AddCategoryButton
from pages.dashboard.content.categories.category_elements import CategoryRow, Category_Header
from pages.dashboard.head_elements import header
from pages.config.style import inputBgErrorColor
import flet as ft



class CategoriesContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []

    def build(self):
        self.column_with_category_rows = ft.Column(
            controls=[],
            spacing=1,
            # height=600,     #scroll не будет работать, если изменить размер окна
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.content_header = header(label_name="Список Категорий", user_role=self.user_role)
        self.view_content.append(self.content_header)

        # resul append to body_content
        req = ReqCategory()
        max_length_category = req.get_max_length()
        name_width = max(max_length_category * 8, 100)  # 7 letter size

        # кнопка "Добавить новую категорию"
        add_button = AddCategoryButton(page=self.page,
                              column_with_rows=self.column_with_category_rows,
                              # передается ссылка на список строк, чтобы к нему добавить новую категорию
                              ).build()
        self.row_1 = ft.Row(
            controls=[add_button],
            alignment=ft.MainAxisAlignment.END,
            # Приживается к правому краю. При изменении размеров окна - сдвигается соответственно
        )
        
        self.view_content.append(self.row_1)


        self.view_content.append(Category_Header(page=self.page, rows_controls=self.column_with_category_rows.controls).build())  # table header

        # ---rows---
        for category, p_cnt in req.category_products_cnt():
            self.column_with_category_rows.controls.append(
                CategoryRow(
                    page=self.page,
                    category=category,
                    p_product_cnt=str(p_cnt),
                    column_with_rows=self.column_with_category_rows,
                )
            )

        self.view_content.append(self.column_with_category_rows)
        # --rows-----------

        self.view_content.append(error_message_categtory)

        return self.view_content