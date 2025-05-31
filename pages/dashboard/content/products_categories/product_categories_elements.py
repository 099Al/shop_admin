import os
from datetime import datetime, date

import flet as ft

from config import settings
from database.models.models import Product
from database.models.result_objects import CategoryProducts
from pages.config.sizes import d_category_product_column_size
from pages.config.style import defaultFontColor, secondaryBgColor, textFieldColor


class CategoryProductsRow(ft.Row):
    def __init__(self, page, element, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        #self.column_with_rows = column_with_rows  # ссылка на список продуктов, чтобы отсюда ее модифицировать

        self.d_column_size = d_category_product_column_size
        #self.d_error_messages = d_error_messages


        self.element: CategoryProducts = element

        self.p_product_id: int = self.element.product_id
        self.p_name: str = self.element.name
        self.p_item_no: str = self.element.item_no
        self.p_img: str = self.element.image_name
        self.p_category_id: int = self.element.category_id
        self.p_category_name: str = self.element.category_name

        self.p_image_path: str = self.element.image_path


        self._init_ui_components()
        self.set_read_view()


    def _init_ui_components(self):
        """Initialize all UI components"""
        # Divider element
        self.el_divider = ft.Container(
            height=self.d_column_size['el_height'],
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )

        # Image handling
        self._init_image_components()
        # Text containers
        self._init_attr_containers()
        # Edit button
        self._init_edit_button()
        # Delete button
        self._init_delete_add_button()
        # Main row controls
        self._init_compile_row()

    def _init_image_components(self):
        # if not os.path.isfile(f"{settings.MEDIA}/original/{self.p_img}.jpeg"):
        #     self.p_img = None

        self._img_start_1 = ft.Image(
                        src=self.p_image_path,
                        width=self.d_column_size['c_image'],
                        height=self.d_column_size['el_height'],
                        fit=ft.ImageFit.CONTAIN
        )

        self._img_start = ft.Column(controls=[self._img_start_1])
        self.r_img = ft.Container(content=self._img_start, padding=ft.padding.only(top=5, bottom=5))

    def _init_attr_containers(self):
        self.r_category_name = ft.Container(width=self.d_column_size['c_category_name'], alignment=ft.alignment.bottom_left)
        self.r_img = ft.Container(width=self.d_column_size['c_image'], alignment=ft.alignment.bottom_left)
        self.r_product_name = ft.Container(width=self.d_column_size['c_name'], alignment=ft.alignment.bottom_left)
        self.r_product_item_no = ft.Container(width=self.d_column_size['c_item_no'], alignment=ft.alignment.bottom_left)

    def _init_edit_button(self):
        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self.set_edit_view)
            )
        ])

        # элемент с редактированием
        self.r_edit_container = ft.Container(
            # bgcolor="orange",
            width=self.d_column_size['c_edit'],
            # padding=ft.padding.only(right=30),
            content=None
        )

    def _init_delete_add_button(self):
        self.r_delete_container = ft.Container(
                scale=0.8,
                margin=ft.margin.only(left=0),
                content=ft.Row(
                    controls=[
                    ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog),
                    ft.IconButton(ft.icons.ADD, on_click=self._add_category)
                ])
            )


    def _init_compile_row(self):
        # сборка элементов в строку
        self.controls = [
           self.r_edit_container,
            ft.Container(
            content=ft.Row(
                controls=[
                    self.el_divider,
                    self.r_category_name,
                    self.el_divider,
                    self.r_img,
                    self.el_divider,
                    self.r_product_name,
                    self.el_divider,
                    self.r_product_item_no,
                    self.el_divider,
                ]
            ),
              border=ft.border.only(bottom=ft.border.BorderSide(0.1, "white")),

            ),
           self.r_delete_container
        ]


    def set_read_view(self):
        self.r_edit_container.content = self.r_content_edit
        self._set_attr_Text(self.p_category_name, self.p_name, self.p_item_no)
        self.r_img.content = self._img_start
        self.r_img.padding = ft.padding.only(top=5, bottom=5)




    def set_edit_view(self, e):
        v_category_id = self.p_category_id
        v_category_name = self.r_category_name.content.value

        self.r_edit_container.content = ft.Row(
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

        self.r_category_name.content = ft.TextField(v_category_name, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor,
                                           text_size=15, multiline=True, max_length=d_category_product_column_size['c_category_name'], max_lines=3)

        self.page.update()

    def _save(self, e):
        pass

    def _cancel(self, e):
        self.set_read_view()
        self.page.update()

    def _add_category(self, e):
        pass

    def delete_dialog(self):
        pass

    def _field(self, text, width, max_lines=2):
        return ft.Text(
            text,
            color=defaultFontColor,
            size=15,
            font_family="cupurum",
            width=width,
            height=self.d_column_size['el_height'],
            max_lines=max_lines,
            overflow=ft.TextOverflow.FADE,  # не работает с max_lines
        )

    def _set_attr_Text(self, category_name, name, item_no):
        self.r_category_name.content = self._field(category_name, self.d_column_size['c_category_name'], max_lines=2)
        self.r_product_name.content = self._field(name, self.d_column_size['c_name'], max_lines=2)
        self.r_product_item_no.content = self._field(item_no, self.d_column_size['c_item_no'], max_lines=1)

