import flet as ft


class AddAdminButton:
    def __init__(self, page, **kwargs):
        #super().__init__()
        self.page = page
        #self.d_width = kwargs["d_width"]
        #self.error_message = kwargs["error_message"]
        #self.column_with_rows = kwargs["column_with_rows"]
        #self.c_elements_index: CategoryElementsIndex = kwargs["elements_index"]

    def build(self):
        return ft.Container(
                content=ft.ElevatedButton("Добавить администратора",
                                          icon=ft.icons.ADD,
                                          on_click=self.add_category),
                margin=ft.margin.only(right=30, top=40),
                # width=250,
            )

    def add_category(self, e):
        pass