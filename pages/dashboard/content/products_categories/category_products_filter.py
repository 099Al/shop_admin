import flet as ft

from pages.config.sizes import d_category_product_column_size
from pages.config.style import textFieldColor
from pages.dashboard.content.products_categories.product_categories_elements import CategoryProductsRow


class CategoryProducts_Filter(ft.Row):
    def __init__(self, page, rows_controls):
        self.page = page
        self.rows_controls: list[CategoryProductsRow] = rows_controls
        self.d_colum_size = d_category_product_column_size

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor=None,
            margin=0,
            padding=0,
            visible=True
        )

    def filter_category(self, e):
        for row in self.rows_controls:
            row.filter_category(e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_item_no.value = ""
        self.tf_filter_product.value = ""
        self.page.update()

    def filter_item_no(self, e):
        for row in self.rows_controls:
            row.filter_item_no(e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_category.value = ""
        self.tf_filter_product.value = ""
        self.page.update()

    def filter_product(self, e):
        for row in self.rows_controls:
            row.filter_product(e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_category.value = ""
        self.tf_filter_item_no.value = ""
        self.page.update()


    def drop_filter(self, e):
        for row in self.rows_controls:
            row.drop_filter()

        self.c_drop_filter.content = None
        self.tf_filter_category.value = ""
        self.tf_filter_item_no.value = ""
        self.page.update()

    def build(self):

        self.icon_drop_filter = ft.IconButton(icon=ft.icons.CANCEL, scale=0.8, on_click=self.drop_filter)

        self.tf_filter_category = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,
                                             color="white", on_submit=self.filter_category)

        self.tf_filter_item_no = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,
                                             color="white", on_submit=self.filter_item_no)

        self.tf_filter_product = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,
                                             color="white", on_submit=self.filter_product)

        self.c_drop_filter = ft.Container(
                        content=None,
                        width=self.d_colum_size["c_dell_add"])

        return ft.Row(
                controls=[
                    ft.Container(content=ft.IconButton(icon=ft.icons.FILTER_ALT, scale=0.8), height=40,
                                 width=self.d_colum_size["c_edit"], alignment=ft.alignment.center_right, padding=0),

                    self.el_divider,
                    ft.Container(
                        content=self.tf_filter_category,
                        width=self.d_colum_size["c_category_name"]),
                    self.el_divider,
                    ft.Container(
                        content=self.tf_filter_item_no,
                        width=self.d_colum_size["c_item_no"]),
                    self.el_divider,
                    ft.Container(
                        content=self.tf_filter_product,
                        width=self.d_colum_size["c_name"]),
                    self.el_divider,
                    self.c_drop_filter
                ],
                vertical_alignment=ft.CrossAxisAlignment.END
        )
