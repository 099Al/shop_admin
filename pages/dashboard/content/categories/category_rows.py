import flet as ft

from database.requests.req_categories import ReqCategory
from pages.style.style import *


class CategoryRow(ft.Row):
    def __init__(self, **kwargs):
        super().__init__()
        self.page = kwargs["page"]
        self.d_width = kwargs["d_width"]
        self.error_message = kwargs["error_message"]
        self.id = kwargs["id"]                 #id категории в БД
        self.p_name = kwargs["p_name"]         #название категории
        self.p_product_cnt = kwargs["p_product_cnt"]   #количество продуктов в категории
        self.p_order = kwargs["p_order"]           #порядковый номер для сортировки

        self.l_elements = kwargs["l_elements"]    #ссылка на список категорий, чтобы отсюда ее модифицировать

        self.error_upd = ft.SnackBar(
            content=ft.Text('категория с таким названием уже существует'),
            bgcolor=inputBgErrorColor
        )

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )

        self.r_name = self.f_field(text=self.p_name, width=self.d_width['c_category'])
        self.r_order = self.f_field(text=self.p_order, width=self.d_width['c_order_sort'])
            # ft.Container(
            #     width=self.d_width['c4'],
            #     content=ft.Text(
            #         self.p_order,
            #         color=defaultFontColor,
            #         size=15,
            #         font_family="cupurum",
            #     ),
            # ),


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

            for x in self.l_elements:
                if x.id == self.id:
                    self.l_elements.remove(x)

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

        self.page.dialog = dlg_delete
        dlg_delete.open = True
        self.page.update()


el_divider = ft.Container(
                height=25,
                width=1,
                bgcolor="white",
                margin=0,
                padding=0
            )

def el_category_header(d_width):
    return ft.Row(
        controls=[
            ft.Container(
                width=d_width["c_edit"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Категории",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c_category"],
                alignment=ft.alignment.bottom_left,
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Количество позиций",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c_cnt"],
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Сортировка",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=d_width["c_order_sort"],
            ),
            el_divider,
        ],
        height=50,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )


class AddCategoryButton:
    def __init__(self, **kwargs):
        #super().__init__()
        self.page = kwargs["page"]
        self.d_width = kwargs["d_width"]
        self.error_message = kwargs["error_message"]
        self.l_elements = kwargs["l_elements"]
        #self.c_elements_index: CategoryElementsIndex = kwargs["elements_index"]

    def build(self):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.ElevatedButton("Добавить категорию",
                                              icon=ft.icons.ADD,
                                              on_click=self.add_category),
                    margin=ft.margin.only(right=30, top=40),
                    #width=250,

                )
            ],
            alignment=ft.MainAxisAlignment.END,
        )

    def add_category(self, e):
        def add_category_handle_yes(e):

            req = ReqCategory()
            category_name = dlg_create.content.content.controls[0].value
            category_order = dlg_create.content.content.controls[1].value
            if category_order.strip() == "":
                category_order = None
            elif not category_order.isdigit():
                category_order = None

            new_id = req.new_category(category_name, category_order)

            if new_id is None:
                self.error_message.open = True
                self.error_message.update()
                return
            else:
                new_row = CategoryRow(
                    page=self.page,
                    d_width=self.d_width,
                    error_message=self.error_message,
                    id=new_id,
                    p_name=category_name,
                    p_order=category_order,
                    p_product_cnt=0,
                    l_elements=self.l_elements,
                )

                #self.c_elements_index.add_element(new_row) #добавление элемента в список
                self.l_elements.append(new_row)

                dlg_create.open = False
                self.page.update()

        def add_category_handle_close(e):
            dlg_create.open = False
            self.page.update()

        dlg_create = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новая категория"),
            content=ft.Container(
                height=80,
                content=ft.Column(
                    controls=[
                        ft.TextField(label="Название", height=40, read_only=False, text_size=15),
                        ft.TextField(label="Номер расположения", height=40, read_only=False, text_size=15),
                    ]
                )
            ),
            actions=[
                ft.TextButton("Yes", on_click=add_category_handle_yes),
                ft.TextButton("No", on_click=add_category_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

        self.page.open(dlg_create)
        # dlg_create.open = True
        self.page.update()



class AddCategoryButton2(ft.ElevatedButton):
    """
    Пример кастомной кнопки
    В content.py оборачиваем данный элемент в Container и двигаем
    # el = ft.Row(controls=[
                #     ft.Container(content=AddCategoryButton(page=self.page), margin=ft.margin.only(right=30, top=40))],
                #             alignment=ft.MainAxisAlignment.END)
                # self.body_content.append(el)
    Внутри данного элемента не работает Container и Row, чтобы задать расположение
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.page = kwargs["page"]
        self.text = "Добавить категорию"
        self.icon = ft.icons.ADD
        self.on_click = self.add_category


    def add_category(self, e):
        pass

