import flet as ft

from database.requests.req_categories import ReqCategory
from pages.config.errors import d_error_messages
from pages.dashboard.content.categories.category_rows import CategoryRow


class AddCategoryButton:
    def __init__(self, page, **kwargs):
        #super().__init__()
        self.page = page


        self.error_message = d_error_messages
        self.column_with_rows = kwargs["column_with_rows"]
        #self.c_elements_index: CategoryElementsIndex = kwargs["elements_index"]

    def build(self):
        return ft.Container(
                    content=ft.ElevatedButton("Добавить категорию",
                                              icon=ft.icons.ADD,
                                              on_click=self.add_category),
                    margin=ft.margin.only(right=30, top=40),
                    #width=250,

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
                    d_width=self.d_column_width,
                    error_message=self.error_message,
                    id=new_id,
                    p_name=category_name,
                    p_order=category_order,
                    p_product_cnt=0,
                    column_with_rows=self.column_with_rows,
                )

                #self.c_elements_index.add_element(new_row) #добавление элемента в список
                self.column_with_rows.controls.append(new_row)

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



# class AddCategoryButton2(ft.ElevatedButton):
#     """
#     Пример кастомной кнопки
#     В content.py оборачиваем данный элемент в Container и двигаем
#     # el = ft.Row(controls=[
#                 #     ft.Container(content=AddCategoryButton(page=self.page), margin=ft.margin.only(right=30, top=40))],
#                 #             alignment=ft.MainAxisAlignment.END)
#                 # self.body_content.append(el)
#     Внутри данного элемента не работает Container и Row, чтобы задать расположение
#     """
#     def __init__(self, **kwargs):
#         super().__init__()
#         self.page = kwargs["page"]
#         self.text = "Добавить категорию"
#         self.icon = ft.icons.ADD
#         self.on_click = self.add_category
#
#
#     def add_category(self, e):
#         pass
