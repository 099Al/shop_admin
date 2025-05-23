import json
import os
import shutil
import uuid
from datetime import datetime, date

import flet as ft

from database.models.models import Product
from database.requests.req_products import ReqProduct
from pages.config.errors import d_error_messages
from pages.config.sizes import pr_name_max_length, pr_item_no_max_length, pr_description_max_length, \
    pr_promo_desc_max_length
from pages.config.sizes import d_product_column_size
from pages.dashboard.content.products.validation import cut_price, is_valid_price, is_valid_date
from pages.config.style import *
from config import settings
import utils.functions as ut


el_divider = ft.Container(
                height=25,
                width=1,
                bgcolor="white",
                margin=0,
                padding=0
            )





class Product_Header:

    def __init__(self, page, rows_controls):
        #self.d_width = d_width
        self.page = page
        self.rows_controls: list[ProductRow] = rows_controls
        self.sort_name_state = 0
        self.sort_item_no_state = 0
        self.sort_price_state = 0
        self.sort_promo_end_state = 0


        self.container_sort_by_name = self._create_sort_cell()
        self.container_sort_by_item_no = self._create_sort_cell()
        self.container_sort_by_price = self._create_sort_cell()
        self.container_sort_by_promo_end = self._create_sort_cell()

    def _create_sort_cell(self):
        return ft.Container(
            content=ft.Text(""),
            alignment=ft.alignment.bottom_left,
            width=20,
            #padding=ft.padding.only(left=20),
            #bgcolor='red'
        )

    def _create_sort_icon(self, rotation):

        if rotation is not None:
            sort_icon = ft.Icon(name=ft.icons.ARROW_RIGHT_ALT, rotate=rotation, color=ft.colors.WHITE, size=20)
        else:
            sort_icon = ft.Text("")

        return ft.Container(
            content=sort_icon,
            alignment=ft.alignment.bottom_right,
            padding=0,
            #bgcolor='orange'
        )


    def _update_sort(self, sort_type, state):

        d_sort_type = {"name": lambda x: x.p_name,
                       "item_no": lambda x: x.p_item_no if x.p_item_no is not None else '0',
                       "price": lambda x: x.p_price if x.p_price is not None else 0,
                       "promo_end": lambda x: x.p_promo_end if x.p_promo_end is not None else date(2000, 1, 1),
                       }

        container = getattr(self, f"container_sort_by_{sort_type}")
        state_attr = f"sort_{sort_type}_state"

        if state == 1:
            container.content = self._create_sort_icon(1.57)
            key = d_sort_type[sort_type]
            self.rows_controls.sort(key=key, reverse=True)
        elif state == 2:
            container.content = self._create_sort_icon(4.71)
            key = d_sort_type[sort_type]
            self.rows_controls.sort(key=key)
        else:
            container.content = self._create_sort_icon(None)
            self.rows_controls.sort(key=lambda x: x.product_id)

        #сдинуть треугольник, если стрелок нет
        container.padding = ft.padding.only(left=0) if state != 0 else ft.padding.only(left=20)
        setattr(self, state_attr, state)
        self.page.update()

    def _reset_other_sort(self, sort_type):
        # Reset all sort states except the one being specified
        for st in ["name", "item_no", "price", "promo_end"]:
            if st != sort_type:
                setattr(self, f"sort_{st}_state", 0)
                container = getattr(self, f"container_sort_by_{st}")
                container.content = ft.Text("")
                container.padding = ft.padding.only(left=20)


    def sort_by(self, e, sort_type):
        self._reset_other_sort(sort_type)
        current_state = getattr(self, f"sort_{sort_type}_state")
        next_state = (current_state + 1) % 3
        self._update_sort(sort_type, next_state)

    def _create_header_cell(self, text, width):
        return ft.Container(
            content=ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
            ),
            width=width,
            alignment=ft.alignment.bottom_left,
        )

    def _create_sortable_header_cell(self, text, width, sort_container, on_click_handler):
        return ft.Container(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            text,
                            color=defaultFontColor,
                            size=15,
                            font_family="cupurum",
                            #bgcolor='blue'
                        ),
                        alignment=ft.alignment.bottom_left
                    ),

                    ft.Row(
                        controls=[
                            sort_container,
                            ft.Container(
                                content=ft.Icon(name=ft.icons.ARROW_DROP_DOWN, size=20),
                                alignment=ft.alignment.bottom_right,
                                padding=0,
                                on_click=on_click_handler,
                                #bgcolor='green'
                            )
                        ],
                        spacing=0
                    )    #два элемента в строку, чтобы прижать к правому краю
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=0,
            width=width,
            #bgcolor='yellow',

        )

    def build(self, d_width):



        header_controls = [
                ft.Container(
                    width=d_width["c_edit"],
                ),
                el_divider,
                self._create_header_cell("Изображение", d_width["c_image"]),
                el_divider,

                self._create_sortable_header_cell("Наименование", d_width["c_name"], self.container_sort_by_name, lambda e: self.sort_by(e, "name")),

                el_divider,

                self._create_sortable_header_cell("Артикул", d_width["с_item_no"], self.container_sort_by_item_no, lambda e: self.sort_by(e, "item_no")),

                el_divider,
                self._create_sortable_header_cell("Цена", d_width["c_price"], self.container_sort_by_price, lambda e: self.sort_by(e, "price")),
                el_divider,
                self._create_header_cell("Описание", d_width["c_desc"]),
                el_divider,
                self._create_header_cell("Цена по Акции", d_width["c_price_promo"]),
                el_divider,
                self._create_sortable_header_cell("Акция до", d_width["c_promo_end"], self.container_sort_by_promo_end, lambda e: self.sort_by(e, "promo_end")),

                el_divider,
                self._create_header_cell("Акция Описание", d_width["c_promo_desc"]),
                el_divider,

            ]

        return ft.Row(
            controls=header_controls,
            height=50,
            vertical_alignment=ft.CrossAxisAlignment.END
        )






class ProductRow(ft.Row):
    def __init__(self, page, product, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список продуктов, чтобы отсюда ее модифицировать

        self.d_column_width = d_product_column_size
        self.d_error_messages = d_error_messages


        self.product: Product = product

        self.product_id: int = self.product.product_id
        self.p_name: str = self.product.name
        self.p_item_no: str = self.product.item_no
        self.p_price: float = self.product.price
        self.p_desc: str = self.product.description
        self.p_promo_price: float = self.product.promo_price
        self.p_promo_end = self.product.promo_expire_date
        self.p_promo_desc: str = self.product.promo_desc
        self.p_img: str = self.product.r_image.image_name if self.product.r_image else None

        self.tmp_image_name = None
        self.flag_delete_image = None

        self._init_ui_components()

        if self.product_id is None:
            self.set_edit_view(None)
        else:
            self.set_read_view()


    def _init_ui_components(self):
        """Initialize all UI components"""
        # Divider element
        self.el_divider = ft.Container(
            height=98,
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
        self._init_delete_button()

        # Main row controls
        self._init_compile_row()




    def _init_image_components(self):
        if not os.path.isfile(f"{settings.MEDIA}/original/{self.p_img}.jpeg"):
            self.p_img = None

        self._img_start_1 = ft.Image(
                        src=f"{settings.MEDIA}/original/{self.p_img}.jpeg" if self.p_img else f"{settings.MEDIA}/default/no_product_photo.jpeg",
                        width=self.d_column_width['c_image'],
                        height=100,
                        fit=ft.ImageFit.CONTAIN
        )

        self._img_start = ft.Column(controls=[self._img_start_1])
        self.r_img = ft.Container(content=self._img_start, padding=ft.padding.only(top=5, bottom=5))

    def _init_attr_containers(self):

        self.r_name = ft.Container(width=self.d_column_width['c_name'], alignment=ft.alignment.bottom_left)
        self.r_item_no = ft.Container(width=self.d_column_width['с_item_no'], alignment=ft.alignment.bottom_left)
        self.r_price = ft.Container(width=self.d_column_width['c_price'], alignment=ft.alignment.bottom_left)
        self.r_desc = ft.Container(width=self.d_column_width['c_desc'], alignment=ft.alignment.bottom_left)
        self.r_promo_price = ft.Container(width=self.d_column_width['c_price'], alignment=ft.alignment.bottom_left)
        self.r_promo_end = ft.Container(width=self.d_column_width['c_promo_end'], alignment=ft.alignment.bottom_left)
        self.r_promo_desc = ft.Container(width=self.d_column_width['c_promo_desc'], alignment=ft.alignment.bottom_left)

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
        self.r_container_icon = ft.Container(
            # bgcolor="orange",
            width=self.d_column_width['c_edit'],
            # padding=ft.padding.only(right=30),
            content=None
        )

    def _init_delete_button(self):
        self.r_delete_container = ft.Container(
                scale=0.8,
                margin=ft.margin.only(left=0),
                content=ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog)
            )

    def _init_compile_row(self):
        # сборка элементов в строку
        self.controls = [
            self.r_container_icon,
            ft.Container(
            content=ft.Row(
                controls=[
                    self.el_divider,
                    self.r_img,
                    self.el_divider,
                    self.r_name,
                    self.el_divider,
                    self.r_item_no,
                    self.el_divider,
                    self.r_price,
                    self.el_divider,
                    self.r_desc,
                    self.el_divider,
                    self.r_promo_price,
                    self.el_divider,
                    self.r_promo_end,
                    self.el_divider,
                    self.r_promo_desc,
                    self.el_divider
                ]
            ),
              border=ft.border.only(bottom=ft.border.BorderSide(0.1, "white")),

            ),
            self.r_delete_container
        ]

    def set_read_view(self):
        self.r_container_icon.content = self.r_content_edit
        self._set_attr_Text(self.p_name, self.p_item_no, self.p_price, self.p_desc,
                            self.p_promo_price, self.p_promo_end, self.p_promo_desc)
        self.r_img.content = self._img_start
        self.r_img.padding = ft.padding.only(top=5, bottom=5)



    def set_edit_view(self, e):
        if self.product_id:
            #тип в строке может меняться
            v_name = self.r_name.content.value
            v_item_no = self.r_item_no.content.value
            v_price: [str, float] = self.r_price.content.value
            v_desc = self.r_desc.content.value
            v_promo_price = self.r_promo_price.content.value
            v_promo_end = self.r_promo_end.content.value
            v_promo_desc = self.r_promo_desc.content.value
        else:
            v_name = ""
            v_item_no = ""
            v_price = ""
            v_desc = ""
            v_promo_price = ""
            v_promo_end = ""
            v_promo_desc = ""

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

        self._init_edit_image_components()

        self.r_name.content = ft.TextField(v_name, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor,text_size=15, multiline=True, max_length=pr_name_max_length, max_lines=3)
        self.r_item_no.content = ft.TextField(v_item_no, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, max_length=pr_item_no_max_length, text_size=15)
        self.r_price.content = ft.TextField(v_price, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_desc.content = ft.TextField(v_desc, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15, multiline=True, max_length=pr_description_max_length)
        self.r_promo_price.content = ft.TextField(v_promo_price, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_promo_end.content = ft.TextField(v_promo_end, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15)
        self.r_promo_desc.content = ft.TextField(v_promo_desc, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor, text_size=15, multiline=True, max_length=pr_promo_desc_max_length)

        self.page.update()



    def _init_edit_image_components(self):
        style_item_button = ft.ButtonStyle(
            color={ft.ControlState.DEFAULT: ft.colors.BLUE_500, },
            bgcolor={ft.ControlState.DEFAULT: "white", }
        )

        # вынесено отдельно, чтобы потом можно было изменить через замену src в другом месте
        self._img_edit_1 = ft.Image(
            src=f"{settings.MEDIA}/original/{self.p_img}.jpeg" if self.p_img else f"{settings.MEDIA}/default/no_product_photo.jpeg",
            width=100,
            height=100,
            opacity=0.5,
            fit=ft.ImageFit.CONTAIN
        )

        _img_edit = ft.Stack(
            controls=[self._img_edit_1,

                      ft.Column(
                          controls=[
                              ft.Container(
                                  content=ft.TextButton(
                                      "Upload",
                                      style=style_item_button,
                                      scale=0.7,
                                      icon=ft.icons.UPLOAD_FILE,
                                      on_click=lambda _: file_picker.pick_files(allow_multiple=False)
                                  )
                              ),
                              ft.Container(
                                  content=ft.TextButton(
                                      "Delete",
                                      style=style_item_button,
                                      scale=0.7,
                                      icon=ft.icons.DELETE_FOREVER,
                                      on_click=self._image_delete
                                  )
                              )
                          ]
                      )

                      ],
            alignment=ft.alignment.center
        )

        self.r_img.content = _img_edit
        self.r_img.padding = ft.padding.only(top=15, bottom=5)

        file_picker = ft.FilePicker(on_result=self._image_upload)
        self.page.overlay.append(file_picker)


    def _image_upload(self, x, **kwargs):
        try:
            allowed_extensions = {'.png', '.jpeg', '.jpg'}
            path_to_src_file = json.loads(x.data)['files'][0]['path']
            ext = os.path.splitext(path_to_src_file)[1].lower()
            if ext not in allowed_extensions:
                error_image = self.d_error_messages["image_error"]
                error_image.open = True
                error_image.update()
            else:
                self.tmp_image_name = f"{uuid.uuid4().hex}_{self.p_name}"
                shutil.copy(path_to_src_file,
                            f"{settings.MEDIA_TMP}/{self.tmp_image_name}.jpeg")  # копируем во временную директорию (settings.MEDIA_TMP)
                self._img_edit_1.src = f"{settings.MEDIA_TMP}/{self.tmp_image_name}.jpeg"
                self.r_img.update()
                self.page.update()

        except Exception as e:
            pass  # пользователь ничего не выбрал


    def _field(self, text, width, max_lines=2):
        return ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
                width=width,
                max_lines=max_lines,
                overflow=ft.TextOverflow.ELLIPSIS,
            )

    def _set_attr_Text(self, name, item_no, price, desc, promo_price, promo_end, promo_desc):
        self.r_name.content = self._field(name, self.d_column_width['c_name'], max_lines=2)
        self.r_item_no.content = self._field(item_no, self.d_column_width['с_item_no'])
        self.r_price.content = self._field(price, self.d_column_width['c_price'])
        self.r_desc.content = self._field(desc, self.d_column_width['c_desc'], max_lines=4)
        self.r_promo_price.content = self._field(promo_price, self.d_column_width['c_price'])
        self.r_promo_end.content = self._field(promo_end, self.d_column_width['c_promo_end'])
        self.r_promo_desc.content = self._field(promo_desc, self.d_column_width['c_promo_desc'], max_lines=4)

    def _image_delete(self, e):
        self._img_edit_1.src = f"{settings.MEDIA}/default/no_product_photo.jpeg"
        self.flag_delete_image = True
        try:
            os.remove(f"{settings.MEDIA_TMP}/{self.tmp_image_name}.jpeg")
        except:
            pass
        self.tmp_image_name = None

        self.r_img.update()
        self.page.update()



    def save(self, e):
        #значение после изменения в поле

        if not self._validate():
            return

        v_name = self.r_name.content.value
        v_item_no = self.r_item_no.content.value
        v_price: [str, float] = self.r_price.content.value
        v_desc = self.r_desc.content.value
        v_promo_price = cut_price(self.r_promo_price.content.value)
        v_promo_end = self.r_promo_end.content.value
        v_promo_desc = self.r_promo_desc.content.value

        if self.product_id == None:
            #новый продукт
            self._handle_new_product_save(v_name, v_item_no, v_price, v_desc, v_promo_price, v_promo_end, v_promo_desc)
        else:
            #редактирование продукта
            self._handle_existing_product_save(v_name, v_item_no, v_price, v_desc, v_promo_price, v_promo_end, v_promo_desc)
            self._handle_image_changes()

        self.set_read_view()
        self.page.update()


    def _handle_image_changes(self):

        req = ReqProduct()
        if self.flag_delete_image:
            old_image_name, upd_img_status = req.delete_image(self.product_id)
            if upd_img_status:
                # update произошел
                if old_image_name:
                    try:
                        os.remove(f"{settings.MEDIA}/original/{old_image_name}.jpeg")
                    except:
                        pass
                self.p_img = None
                self._img_start_1.src = f"{settings.MEDIA}/default/no_product_photo.jpeg"
                self.r_img.content = self._img_start

            self.flag_delete_image = False

        if self.tmp_image_name:  # если была загружена новая картинка
            tmp_path = f"{settings.MEDIA_TMP}/{self.tmp_image_name}.jpeg"
            self.p_img = ut.image_to_16digit_hash(tmp_path, self.product_id)
            old_image_name, upd_img_status = req.update_image(self.product_id, self.p_img)
            if upd_img_status:
                # update произошел. Удаляем старое изображение
                if old_image_name:
                    try:
                        os.remove(f"{settings.MEDIA}/original/{old_image_name}.jpeg")
                    except:
                        pass
                shutil.copy(tmp_path, f"{settings.MEDIA}/original/{self.p_img}.jpeg")
                os.remove(tmp_path)
                self.tmp_image_name = None

                self._img_start_1.src = f"{settings.MEDIA}/original/{self.p_img}.jpeg"


    def _handle_existing_product_save(self, name, item_no, price, desc, promo_price, promo_end, promo_desc):
        req = ReqProduct()
        is_exists_product = req.check_product_exists(name, item_no, self.product_id)

        if is_exists_product:
            key = "error_pk_item_no" if is_exists_product == 1 else "error_pk_name"
            error_validation = self.d_error_messages[key]
            error_validation.open = True
            error_validation.update()
        else:
            self._update_existing_product(req, name, item_no, price, desc, promo_price, promo_end, promo_desc)


    def _update_existing_product(self, req, name, item_no, price, desc, promo_price, promo_end, promo_desc):
        d_new_values = {
            "name": name,
            "item_no": item_no,
            "price": float(price) if price else None,
            "description": desc,
            "promo_price": float(promo_price) if promo_price else None,
            "promo_expire_date": is_valid_date(promo_end) if promo_end else None,
            "promo_desc": promo_desc
        }

        # Проверка на изменения в любом из полей
        flag_update_attr = any(
            getattr(self.product, key) != value
            for key, value in d_new_values.items()
        )

        if flag_update_attr and req.update_product(self.product_id, **d_new_values):
            self._update_product_attributes(name, item_no, price, desc, promo_price, promo_end, promo_desc)


    def _handle_new_product_save(self, v_name, v_item_no, v_price, v_desc, v_promo_price, v_promo_end, v_promo_desc):
            new_product = Product(
                name=v_name,
                item_no=v_item_no,
                price=float(v_price) if v_price else None,
                description=v_desc,
                promo_price=float(v_promo_price) if v_promo_price else None,
                promo_expire_date=is_valid_date(v_promo_end) if v_promo_end else None,
                promo_desc=v_promo_desc
            )

            req = ReqProduct()

            self.product_id = req.add_product(new_product)

            if self.product_id is None:
                error_validation = self.d_error_messages["insert_error"]
                error_validation.open = True
                error_validation.update()
                return

            if self.tmp_image_name:
                self.p_img = ut.image_to_16digit_hash(f"{settings.MEDIA_TMP}/{self.tmp_image_name}.jpeg",
                                                      self.product_id)
                req.add_image(self.product_id, self.tmp_image_name)
                shutil.copy(f"{settings.MEDIA_TMP}/{self.tmp_image_name}.jpeg",
                            f"{settings.MEDIA}/original/{self.p_img}.jpeg")
                os.remove(f"{settings.MEDIA_TMP}/{self.tmp_image_name}.jpeg")
                self.tmp_image_name = None
                self._img_start_1.src = f"{settings.MEDIA}/original/{self.p_img}.jpeg"



    def _update_product_attributes(self, name, item_no, price, desc, promo_price, promo_end, promo_desc):
        self.p_name = name
        self.p_item_no = item_no
        self.p_price = float(price) if price else None
        self.p_desc = desc
        self.p_promo_price = float(promo_price) if promo_price else None
        self.p_promo_end = is_valid_date(promo_end) if promo_end else None
        self.p_promo_desc = promo_desc


    def cancel(self, e):
        # self.r_img.content = self._img_start
        # self.r_img.padding = ft.padding.only(top=5, bottom=5)
        # self._set_attr_Text(self.p_name, self.p_item_no, self.p_price, self.p_desc, self.p_promo_price, self.p_promo_end, self.p_promo_desc)
        # self.r_container_icon.content = self.r_content_edit

        self.set_read_view()
        self.flag_delete_image = False

        if os.path.isfile(f"{settings.MEDIA_TMP}/{self.tmp_image_name}"):
            os.remove(f"{settings.MEDIA_TMP}/{self.tmp_image_name}")

        self.page.update()


    def delete_dialog(self, e):
        def delete_category_handle_yes(e):
            req = ReqProduct()

            image_name, upd_img_status = req.delete_image(self.product_id)

            if image_name:
                try:
                    os.remove(f"{settings.MEDIA}/original/{image_name}.jpeg")
                except:
                    pass

            req.delete_product(self.product_id)



            for product_row in self.column_with_rows.controls:
                if product_row.product_id == self.product_id:
                    self.column_with_rows.controls.remove(product_row)

            dlg_delete.open = False
            self.page.update()

        def delete_category_handle_close(e):
            dlg_delete.open = False
            self.page.update()

        dlg_delete = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение"),
            content=ft.Text("Вы действительно хотите удалить продукт?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_category_handle_yes),
                ft.TextButton("No", on_click=delete_category_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

        self.page.open(dlg_delete)
        # dlg_delete.open = True
        self.page.update()



    def _validate(self):
        v_name = self.r_name.content.value
        v_item_no = self.r_item_no.content.value
        v_price = self.r_price.content.value
        v_desc = self.r_desc.content.value
        v_promo_price = self.r_promo_price.content.value
        v_promo_end = self.r_promo_end.content.value  #если из БД, то тип datetime, если прописываем, то string
        v_promo_desc = self.r_promo_desc.content.value

        flag_valid = True

        if v_price and not is_valid_price(cut_price(v_price)):
            self.r_price.content = ft.TextField(v_price, color="white", bgcolor=secondaryBgColor, border_color=errorFieldColor, text_size=15)
            flag_valid = False
        else: #чтобы вернуть в начальное состояние после исправления
            self.r_price.content = ft.TextField(v_price, color="white", bgcolor=secondaryBgColor,border_color=textFieldColor, text_size=15)
        if v_promo_price and not is_valid_price(cut_price(v_promo_price)):
            self.r_promo_price.content = ft.TextField(v_promo_price, color="white", bgcolor=secondaryBgColor, border_color=errorFieldColor, text_size=15)
            flag_valid = False
        else:
            self.r_promo_price.content = ft.TextField(v_promo_price, color="white", bgcolor=secondaryBgColor,border_color=textFieldColor, text_size=15)

        if v_promo_end and not is_valid_date(v_promo_end):
            self.r_promo_end.content = ft.TextField(v_promo_end, color="white", bgcolor=secondaryBgColor, border_color=errorFieldColor, text_size=15)
            flag_valid = False
        else:
            self.r_promo_end.content = ft.TextField(v_promo_end, color="white", bgcolor=secondaryBgColor,border_color=textFieldColor, text_size=15)

        if not flag_valid:
            error_validation = self.d_error_messages["validation_error"]
            error_validation.open = True
            error_validation.update()

            self.page.update()

        return flag_valid


    def filter_name(self, text):
        if self.p_name is None or self.p_name == "":
            lv_name = ""
        else:
            lv_name = self.p_name

        if text.lower() in lv_name.lower():
            self.visible = True
        else:
            self.visible = False

    def filter_item_no(self, text):
        if self.p_item_no is None or self.p_item_no == "":
            lv_item_no = ""
        else:
            lv_item_no = self.p_item_no

        if text.lower() in lv_item_no.lower():
            self.visible = True
        else:
            self.visible = False

    def drop_filter(self):
        self.visible = True
