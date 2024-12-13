import flet as ft

class CustomCategoryRow(ft.Row):
    def __init__(self, text):
        super().__init__()
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(
            visible=False, icon=ft.icons.SAVE, on_click=self.save
        )
        self.text_view = ft.Text(text, size=30,
                                 bgcolor=ft.colors.AMBER_500,
                                 )
        self.text_edit =  ft.Container(
                            content=ft.TextField("AAAAAAAAAAAAAAAA", height=60, read_only=False, text_size=30),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,

                            bgcolor=ft.colors.AMBER,
                            width=150,
                            height=70,
                            border_radius=10,
                        )


        self.controls = [
            self.edit_button,
            self.save_button,
            self.text_view,
            self.text_edit,
        ]

    def edit(self, e):
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()

    def save(self, e):
        self.edit_button.visible = True
        self.save_button.visible = False
        self.text_view.visible = True
        self.text_edit.visible = False
        self.text_view.value = self.text_edit.value
        self.update()

