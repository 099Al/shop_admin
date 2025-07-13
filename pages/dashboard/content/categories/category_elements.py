import flet as ft

from database.models.models import Category
from database.requests.req_categories import ReqCategory
from pages.config.errors import error_message_categtory, error_message_category_validate_order
from pages.config.sizes import d_category_width
from pages.config.style import *


class CategoryRow(ft.Row):
    def __init__(self, page, category, product_cnt, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список категорий, чтобы отсюда ее модифицировать

        self.d_width = d_category_width
        self.error_message = error_message_categtory
        self.error_message_category_validate_order = error_message_category_validate_order

        self.category: Category = category
        self.id = category.id                   #id категории в БД
        self.name = category.name             #название категории
        self.order_sort = category.order_number    #порядковый номер для сортировки
        self.product_cnt = product_cnt      # количество продуктов в категории

        self.el_divider = ft.Container(
            height=25,
            #expand=True,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0,
            content=ft.Text(""),
        )

        #init attr containers
        self.r_name = ft.Container(width=self.d_width['name'], alignment=ft.alignment.bottom_left)
        self.r_cnt = ft.Container(width=self.d_width['product_cnt'], alignment=ft.alignment.bottom_left)
        self.r_order = ft.Container(width=self.d_width['order_sort'], alignment=ft.alignment.bottom_left)

        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self._edit_view)
            )
        ])

        #элемент с редактированием
        self.r_container_icon = ft.Container(
            # bgcolor="orange",
            width=self.d_width['edit'],
            # padding=ft.padding.only(right=30),
            content=self.r_content_edit if self.name != "default" else None  #default нельзя изменить
        )

        #init delete button
        self.r_delete_container = ft.Container(
                scale=0.8,
                margin=ft.margin.only(left=0),
                padding=ft.padding.only(right=15),

                content=ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog) if self.name != "default" else None  #default нельзя удалить
            )


        #сборка элементов в строку
        self.controls = [
            self.r_container_icon,
            self.el_divider,
            self.r_name,
            self.el_divider,
            self.r_cnt,
            self.el_divider,
            self.r_order,
            self.el_divider,
            self.r_delete_container
        ]

        self._set_read_view()


    def _set_read_view(self):
        self.r_container_icon.content = self.r_content_edit
        self.r_name.content = ft.Text(self.name, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_cnt.content = ft.Text(self.product_cnt, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_order.content = ft.Text(self.order_sort, color=defaultFontColor, size=15, font_family="cupurum")



    def _f_field(self, text, width):
        return ft.Container(
            content=ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
                overflow=ft.TextOverflow.ELLIPSIS,
                max_lines=1
            ),
            # height=25,
            width=width,
            alignment=ft.alignment.bottom_left,
            #bgcolor=ft.colors.DEEP_ORANGE_800
        )

    def _edit_view(self, e):
        v_text = self.r_name.content.value
        v_order = self.r_order.content.value
        # self.category_text = v_text  # save text
        self.name = v_text
        self.order_sort = v_order

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
                             content=ft.IconButton(ft.icons.SAVE, on_click=self._save)),
                ft.Container(margin=ft.margin.only(left=0),
                             scale=0.8,
                             # bgcolor="green",
                             content=ft.IconButton(ft.icons.CANCEL, on_click=self._cancel))
            ]
        )
        self.r_container_icon.update()
        self.r_name.update()
        self.r_order.update()

        # self.page.update()

    def _save(self, e):
        v_text = self.r_name.content.value
        v_order = self.r_order.content.value

        if v_order and not v_order.isdigit():
            self.error_message_category_validate_order.open = True
            self.page.update()
            return

        req = ReqCategory()
        upd_res = req.update_category(self.name, v_text, v_order)

        if upd_res is None:
            self.error_message.open = True
            self.error_message.update()
        else:
            self.r_container_icon.content = self.r_content_edit
            self.r_container_icon.update()

        # обновление параметров Category внутри Category Row
        self.category = req.get_category_by_id(self.id)
        self.name = v_text
        self.order_sort = v_order

        self._set_read_view()
        self.page.update()

    def _cancel(self, e):
        self.r_container_icon.content = self.r_content_edit
        self._set_read_view()
        self.page.update()




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


