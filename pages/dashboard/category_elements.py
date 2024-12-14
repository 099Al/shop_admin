import flet as ft

from database.connect import DataBase
from database.requests.req_products import ReqCategory
from pages.style.style import *


class CategoryRow(ft.Row):
    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs["id"]
        self.p_name = kwargs["p_name"]
        self.p_cnt = kwargs["p_cnt"]
        self.name_width = kwargs["name_width"]
        self.page = kwargs["page"]
        self.out_controls = kwargs["controls"]
        self.indx = kwargs["index"]
        self.index_of_elements = kwargs["index_of_elements"]

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )

        self.r_name = ft.Container(
            content=ft.Text(
                self.p_name,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
            ),
            # height=25,
            width=self.name_width,
            alignment=ft.alignment.bottom_left,
        )

        self.r_content_edit = ft.Row(controls=[
            ft.Container(
                scale=0.8,
                # bgcolor="blue",
                margin=ft.margin.only(left=47),
                content=ft.IconButton(ft.icons.EDIT, on_click=self.edit)
            )
        ])

        self.r_container_icon = ft.Container(
            # bgcolor="orange",
            width=80,
            # padding=ft.padding.only(right=30),
            content=self.r_content_edit
        )

        self.controls = [
            self.r_container_icon,
            self.el_divider,
            self.r_name,
            self.el_divider,
            ft.Container(
                width=150,
                content=ft.Text(
                    self.p_cnt,
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
            ),
            self.el_divider,
            ft.Container(
                scale=0.8,
                margin=ft.margin.only(left=0),
                content=ft.IconButton(ft.icons.DELETE, on_click=self.delete_dialog)
            ),
        ]

        #self.category_text = ""  # for save state

    def edit(self, e):
        v_text = self.r_name.content.value
        # self.category_text = v_text  # save text
        self.p_name = v_text
        self.r_name.content = ft.TextField(v_text, color="white", bgcolor=secondaryBgColor, border_color=textFieldColor,
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

        # self.page.update()

    def save(self, e):
        v_text = self.r_name.content.value

        db = DataBase()
        req = ReqCategory(db)
        req.update_category(self.p_name, v_text)

        self.r_container_icon.content = self.r_content_edit
        self.r_name.content = ft.Text(v_text, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_container_icon.update()
        self.r_name.update()
        # self.page.update()

    def cancel(self, e):
        self.r_container_icon.content = self.r_content_edit
        self.r_name.content = ft.Text(self.p_name, color=defaultFontColor, size=15, font_family="cupurum")
        self.r_container_icon.update()
        self.r_name.update()
        # self.page.update()




    def delete_dialog(self, e):
        def delete_category_handle_yes(e):
            db = DataBase()
            req = ReqCategory(db)
            req.delete_category(self.id)
            del self.out_controls[self.index_of_elements[self.indx]]
            del self.index_of_elements[self.indx]         #перенеумерация элементов. т.к. list controls уменьшился. На этот словарь и list ссылваются все элементы
            for i, x in enumerate(self.index_of_elements):
                self.index_of_elements[x] = i
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

def el_header(name_width):
    return ft.Row(
        controls=[
            ft.Container(
                width=80,
            ),
            el_divider,
            ft.Container(
                content=ft.Text(
                    "Категории",
                    color=defaultFontColor,
                    size=15,
                    font_family="cupurum",
                ),
                width=name_width,
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
                width=150,
            ),
            el_divider,
        ],
        height=50,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )




def add_category():
    pass

def el_add_category():
    return ft.Row(
                        controls=[
                            ft.Container(
                            content=ft.ElevatedButton("Добавить категорию",
                                                      icon=ft.icons.ADD,
                                                      on_click=add_category()),
                            margin=ft.margin.only(right=30, top=40),
                            ),
                                  ],
                        alignment=ft.MainAxisAlignment.END,

                    )

