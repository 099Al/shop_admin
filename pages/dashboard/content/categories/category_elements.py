import flet as ft

from database.models.models import Category
from database.requests.req_categories import ReqCategory
from pages.config.errors import error_message_categtory
from pages.config.sizes import d_category_width
from pages.config.style import *



el_divider = ft.Container(
                height=25,
                width=1,
                bgcolor="white",
                margin=0,
                padding=0
            )

class Category_Header:
    def __init__(self, page, rows_controls):
        super().__init__()
        self.page = page
        self.rows_controls: list[CategoryRow] = rows_controls
        self.d_category_width = d_category_width

    def _create_header_cell(self, text, width, visible=True):
        return ft.Container(
            content=ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
            ),
            width=width,
            alignment=ft.alignment.bottom_left,
            visible=visible
        )

    def build(self):
        category_controls = [
                ft.Container(
                    width=d_category_width["c_edit"],
                ),
                el_divider,
                self._create_header_cell("Категории", d_category_width["c_category"]),
                el_divider,
                self._create_header_cell("Количество позиций", d_category_width["c_cnt"]),
                el_divider,
                self._create_header_cell("Сортировка", d_category_width["c_order_sort"]),
                el_divider,
            ]

        return ft.Row(
                controls=category_controls,
                height=50,
                vertical_alignment=ft.CrossAxisAlignment.END,
            )





class CategoryRow(ft.Row):
    def __init__(self, page, category, p_product_cnt, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список категорий, чтобы отсюда ее модифицировать

        self.d_width = d_category_width
        self.error_message = error_message_categtory

        self.category: Category = category
        self.id = category.id                   #id категории в БД
        self.p_name = category.name             #название категории
        self.p_order = category.order_number    #порядковый номер для сортировки
        self.p_product_cnt = p_product_cnt  # количество продуктов в категории

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )

        self.r_name = self.f_field(text=self.p_name, width=self.d_width['c_category'])
        self.r_order = self.f_field(text=self.p_order, width=self.d_width['c_order_sort'])



        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self.edit)
            )
        ])

        #элемент с редактированием
        self.r_container_icon = ft.Container(
            # bgcolor="orange",
            width=self.d_width['c_edit'],
            # padding=ft.padding.only(right=30),
            content=self.r_content_edit if self.p_name != "default" else None  #default нельзя изменить
        )

        #сборка элементов в строку
        self.controls = [
            self.r_container_icon,
            self.el_divider,
            self.r_name,
            self.el_divider,
            ft.Container(
                width=self.d_width['c_cnt'],
                content=ft.Text(
                    self.p_product_cnt,
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
            ),
            self.el_divider,
            self.r_order,
            self.el_divider,
            ft.Container(
                scale=0.8,
                margin=ft.margin.only(left=0),

                content=ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog) if self.p_name != "default" else None  #default нельзя удалить
            ),
        ]

        #self.category_text = ""  # for save state

    def f_field(self, text, width):
        return ft.Container(
            content=ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
            ),
            # height=25,
            width=width,
            alignment=ft.alignment.bottom_left,
            #bgcolor=ft.colors.DEEP_ORANGE_800
        )

    def edit(self, e):
        v_text = self.r_name.content.value
        v_order = self.r_order.content.value
        # self.category_text = v_text  # save text
        self.p_name = v_text
        self.p_order = v_order

        self.r_name.content = ft.TextField(v_text, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor,
                                           text_size=15)

        self.r_order.content = ft.TextField(v_order, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor,
                                           text_size=15)

        self.r_container_icon.content = ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                ft.Container(margin=ft.margin.all(0),
                             padding=ft.padding.all(0),
                             adaptive=True,
                             scale=0.8,
                             # bgcolor="red",
                             content=ft.IconButton(ft.icons.SAVE, on_click=self.save)),
                ft.Container(margin=ft.margin.only(left=0),
                             scale=0.8,
                             # bgcolor="green",
                             content=ft.IconButton(ft.icons.CANCEL, on_click=self.cancel))
            ]
        )
        self.r_container_icon.update()
        self.r_name.update()
        self.r_order.update()

        # self.page.update()

    def save(self, e):
        v_text = self.r_name.content.value
        v_order = self.r_order.content.value

        req = ReqCategory()
        upd_res = req.update_category(self.p_name, v_text, v_order)

        if upd_res is None:
            self.error_message.open = True
            self.error_message.update()
            #self.r_name.content = ft.Text(self.p_name, color=defaultFontColor, size=15, font_family="cupurum")
            self.r_name.content = ft.TextField(self.p_name, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
            self.r_order.content = ft.TextField(self.p_order, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        else:
            self.r_name.content = ft.Text(v_text, color=defaultFontColor, size=15, font_family="cupurum")
            self.r_order.content = ft.Text(v_order, color=defaultFontColor, size=15, font_family="cupurum")
            self.r_container_icon.content = self.r_content_edit
            self.r_container_icon.update()


        self.r_name.update()
        self.r_order.update()
        # self.page.update()

    def cancel(self, e):
        self.r_container_icon.content = self.r_content_edit
        self.r_name.content = ft.Text(self.p_name, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_order.content = ft.Text(self.p_order, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_container_icon.update()
        self.r_name.update()
        self.r_order.update()
        # self.page.update()




    def delete_dialog(self, e):
        def delete_category_handle_yes(e):
            req = ReqCategory()
            req.delete_category_cascade(self.id)

            for category_row in self.column_with_rows.controls:
                if category_row.id == self.id:
                    self.column_with_rows.controls.remove(category_row)

            dlg_delete.open = False
            self.page.update()

        def delete_category_handle_close(e):
            dlg_delete.open = False
            self.page.update()

        dlg_delete = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение"),
            content=ft.Text("Вы действительно хотите удалить категорию?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_category_handle_yes),
                ft.TextButton("No", on_click=delete_category_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

        self.page.open(dlg_delete)
        #dlg_delete.open = True
        self.page.update()


