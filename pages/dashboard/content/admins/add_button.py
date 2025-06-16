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
                                          on_click=self.add_admin),
                margin=ft.margin.only(right=30, top=40),
                # width=250,
            )

    def add_admin(self, e):

        def add_admin_handle_yes(e):
            self.page.add(ft.Text("Yes was clicked"))
            self.page.update()

        def add_admin_handle_close(e):
            dlg_create.open = False
            self.page.update()


        dlg_create = ft.AlertDialog(
            modal=True,
            title=ft.Text("Введите данные пользователя"),
            content=ft.Container(
                height=110,
                content=ft.Column(
                    controls=[
                        ft.TextField(label="Телефон", height=40, read_only=False, text_size=15),
                        ft.Text(value="или", height=15, size=10),
                        ft.TextField(label="Telegram", height=40, read_only=False, text_size=15),

                    ]
                )
            ),
            actions=[
                ft.TextButton("Yes", on_click=add_admin_handle_yes),
                ft.TextButton("No", on_click=add_admin_handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

        self.page.open(dlg_create)
        # dlg_create.open = True
        self.page.update()