from database.requests.req_categories import ReqCategory
from pages.config.errors import error_message_categtory, error_message_category_validate_order
from pages.config.sizes import d_category_width
from pages.dashboard.content.categories.add_category_button import AddCategoryButton
from pages.dashboard.content.categories.category_elements import CategoryRow
from pages.dashboard.content.header import GenericHeader
from pages.dashboard.head_elements import header
import flet as ft



class CategoriesContent:

    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []
        self.field_definitions_header = [
            {"label": "", "field_name": "edit", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Название", "field_name": "name", "sort_attr": "name", "is_sortable": True, "type": str},
            {"label": "Количество товаров", "field_name": "product_cnt", "sort_attr": None, "is_sortable": False, "type": str},
            {"label": "Порядковый\nномер", "field_name": "order_sort", "sort_attr": "order_sort", "is_sortable": True, "type": int},
        ]

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

        self.column_1 = ft.Column(
            controls=[
                # Category_Filter(self.page, self.column_with_category_rows.controls, d_category_width).build(),
                GenericHeader(
                    self.page,
                    self.column_with_category_rows.controls,
                    self.field_definitions_header,
                    d_category_width,
                    'id',
                    int,
                    False
                ).build(),
                # Category_Header(self.page, self.column_with_category_rows.controls).build(),
                self.column_with_category_rows
            ],
            expand=True  #без expand scroll не работает
        )

        # ---rows---
        for category, p_cnt in req.category_products_cnt():
            self.column_with_category_rows.controls.append(
                CategoryRow(
                    page=self.page,
                    category=category,
                    product_cnt=str(p_cnt),
                    column_with_rows=self.column_with_category_rows
                )
            )

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.AUTO
                                 )

        self.view_content.append(self.row_scroll)
        # --rows-----------

        self.view_content.append(error_message_categtory)
        self.view_content.append(error_message_category_validate_order)

        return self.view_content