import flet as ft

from database.models.result_objects import CategoryProducts

from database.requests.req_catgprod import ReqCategoryProduct
from pages.config.errors import d_error_messages_ctg_prod
from pages.config.sizes import d_category_product_column_size
from pages.config.style import defaultFontColor, textFieldColor


class CategoryProductsRow(ft.Row):
    def __init__(self, page, element, column_with_rows, **kwargs):
        super().__init__()
        self.page = page
        self.column_with_rows = column_with_rows  # ссылка на список продуктов, чтобы отсюда ее модифицировать

        self.d_column_size = d_category_product_column_size
        #self.d_error_messages = d_error_messages


        self.element: CategoryProducts = element

        self.product_id: int = self.element.product_id
        self.name: str = self.element.name
        self.item_no: str = self.element.item_no
        self.image: str = self.element.image_name
        self.category_id: int = self.element.category_id
        self.category_name: str = self.element.category_name

        self.image_path: str = self.element.image_path



        self.is_new_category = kwargs.get('is_new_category', False)

        self.l_categories = kwargs.get('l_categories', [])
        self.d_categories = kwargs.get('d_categories', {})

        self._init_ui_components()

        if self.is_new_category:
            self.set_edit_view(None)
        else:
            self.set_read_view()

        #self.set_read_view()


    def __repr__(self):
        return f'CategoryProductsRow(product_id={self.product_id}, category_id={self.category_id}, name={self.name}, item_no={self.item_no})'


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
                        src=self.image_path,
                        width=self.d_column_size['image'],
                        height=self.d_column_size['el_height'],
                        fit=ft.ImageFit.CONTAIN
        )

        self._img_start = ft.Column(controls=[self._img_start_1])
        self.r_img = ft.Container(content=self._img_start, padding=ft.padding.only(top=5, bottom=5))

    def _init_attr_containers(self):
        self.r_category_name = ft.Container(width=self.d_column_size['category_name'], alignment=ft.alignment.bottom_left)

        self.r_product_item_no = ft.Container(width=self.d_column_size['item_no'], alignment=ft.alignment.bottom_left)
        self.r_product_name = ft.Container(width=self.d_column_size['name'], alignment=ft.alignment.bottom_left)
        self.r_img = ft.Container(width=self.d_column_size['image'], alignment=ft.alignment.bottom_left)



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
            width=self.d_column_size['edit'],
            # padding=ft.padding.only(right=30),
            content=None
        )

    def _init_delete_add_button(self):
        self.r_delete_container = ft.Container(
                scale=0.8,
                margin=ft.margin.only(left=0),
                padding=ft.padding.only(right=15),
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
                    self.r_product_item_no,
                    self.el_divider,
                    self.r_product_name,
                    self.el_divider,
                    self.r_img,
                    self.el_divider,
                ]
            ),
              border=ft.border.only(bottom=ft.border.BorderSide(0.1, "white")),

            ),
           self.r_delete_container
        ]


    def set_read_view(self):
        self.r_edit_container.content = self.r_content_edit

        self.r_category_name.content = self._field(self.category_name, self.d_column_size['category_name'], max_lines=2)
        self.r_product_name.content = self._field(self.name, self.d_column_size['name'], max_lines=2)
        self.r_product_item_no.content = self._field(self.item_no, self.d_column_size['item_no'], max_lines=1)


        self.r_img.content = self._img_start
        self.r_img.padding = ft.padding.only(top=5, bottom=5)




    def set_edit_view(self, e):
        if e:
            v_category_id = self.category_id
            v_category_name = self.r_category_name.content.value
        else:
            v_category_name = None

            self.r_product_name.content = self._field(self.name, self.d_column_size['name'], max_lines=2)
            self.r_product_item_no.content = self._field(self.item_no, self.d_column_size['item_no'], max_lines=1)


            self.r_img.content = self._img_start



        self.dd_menu = ft.Dropdown(
            width=self.d_column_size['category_name'],
            editable=False,
            border_color=textFieldColor,
            color="white",
            hint_text=v_category_name,
            hint_style=ft.TextStyle(font_family="cupurum", size=15, color="white"),
            menu_width=self.d_column_size['category_name'],
            menu_height=300,
            options=self.l_categories,

            on_change=self._handle_category_change
        )

        self.r_category_name.content = self.dd_menu

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


        self.page.update()

    def _save(self, e):
        new_category_id = int(self.dd_menu.value)

        req_catg = ReqCategoryProduct()
        is_prodict_exist_in_category = req_catg.check_if_prodict_exist_in_category(new_category_id, self.product_id)

        if is_prodict_exist_in_category:
            d_error_messages_ctg_prod.content = ft.Text(f"Товар уже добавлен в категорию {self.d_categories[new_category_id]}")
            d_error_messages_ctg_prod.open = True
            #d_error_messages_ctg_prod.update()
            self.page.update()
            return

        if self.category_id:
            req_catg.update_category_product(self.category_id, new_category_id, self.product_id)
        else:
            req_catg.add_category_product(new_category_id, self.product_id)

        self.category_id = new_category_id
        self.category_name = self.d_categories[new_category_id]
        self.r_category_name.content = self._field(self.category_name, self.d_column_size['category_name'], max_lines=2)
        self.set_read_view()

        self.page.update()




    def _cancel(self, e):
        if self.is_new_category:
            self.column_with_rows.controls.remove(self)

        self.set_read_view()
        self.page.update()

    def _add_category(self, e):

        position = next((i for i, element in enumerate(self.column_with_rows.controls) if element.category_id == self.category_id and element.product_id == self.product_id), -1)
        #cur_element = self.column_with_rows.controls[position]

        new_element = CategoryProducts(
            category_name=None,
            category_id=None,
            product_id=self.element.product_id,
            name=self.element.name,
            item_no=self.element.item_no,
            image_name=self.element.image_name
        )

        new_row = CategoryProductsRow(
            page=self.page,
            element=new_element,
            column_with_rows=self.column_with_rows,
            d_categories=self.d_categories,
            l_categories=self.l_categories,
            is_new_category=True
        )
        self.column_with_rows.controls.insert(position+1, new_row)

        self.page.update()

    def delete_dialog(self, e):
        def delete_category_product_handle_yes(e):
            req = ReqCategoryProduct()

            req.delete_category_product(self.category_id, self.product_id)

            self.column_with_rows.controls.remove(self)

            dlg_delete.open = False
            self.page.update()


        def delete_category_product_handle_close(e):
            dlg_delete.open = False
            self.page.update()

        dlg_delete = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение"),
            content=ft.Text("Вы действительно хотите удалить товар из категории?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_category_product_handle_yes),
                ft.TextButton("No", on_click=delete_category_product_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(dlg_delete)
        self.page.update()

    def _field(self, text, width, max_lines=2):
        return ft.Text(
            text,
            color=defaultFontColor,
            size=15,
            font_family="cupurum",
            width=width,
            max_lines=max_lines,
            overflow=ft.TextOverflow.FADE,  # не работает с max_lines
            text_align=ft.TextAlign.START
        )




    def _handle_category_change(self, e):
        pass




