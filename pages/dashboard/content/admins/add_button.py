import flet as ft

from database.models.models import Client, Admin
from database.requests.req_admins import ReqAdmins
from database.requests.req_clients import ReqClients
from pages.config.errors import d_error_messages_admin
from pages.dashboard.content.admins.admins_elements import AdminRow


class AddAdminButton:
    def __init__(self, page, column_with_rows, **kwargs):
        self.page = page
        self.error_messages = d_error_messages_admin
        self.column_with_rows = column_with_rows


    def build(self):
        return ft.Container(
                content=ft.ElevatedButton("Добавить администратора",
                                          icon=ft.icons.ADD,
                                          on_click=self.add_admin),
                margin=ft.margin.only(right=30, top=40),
                # width=250,
            )

    def add_admin(self, e):

        req = ReqAdmins()
        req_user = ReqClients()

        def dialog_close(dialog):
            dialog.open = False
            self.page.update()

        def confirm_admin_handle_yes(dialog, client: Client):

            new_admin = Admin(
                telegram_id=client.telegram_id,
                telegram_name=client.telegram_name,
                telegram_link=client.telegram_link,
                name=client.name,
                phone=client.phone,
                email=client.email,
                role="no_role",   #todo: Роли должны задаваться через Enum  AdminRoles
            )

            cur_session = req.get_session()
            cur_session.add(new_admin)
            cur_session.commit()

            res = req_user.update_client(client.telegram_id, type="admin")  #todo: вынести тип через enum

            dialog.open = False

            roles = [ft.DropdownOption(key=str(role), text=str(role)) for role in req.get_all_roles()]
            new_admin_row = AdminRow(self.page, new_admin, roles, self.column_with_rows)

            self.column_with_rows.controls.insert(0, new_admin_row)

            self.page.update()


        def add_admin_handle_yes(e):
            phone = dlg_create.content.content.controls[0].value.replace(" ", "")
            telegram_name = dlg_create.content.content.controls[2].value.replace(" ", "")

            #телефон в приоритете
            client = None
            if phone:
                admin = req.get_admin_by_phone(phone)
                if admin:
                    self.error_messages["admin_exists"].open = True
                    self.page.update()
                    return
                else:
                    client = req_user.get_client_by_phone(phone)

            elif telegram_name:
                admin = req.get_admin_by_telegram_name(telegram_name)
                if admin:
                    self.error_messages["admin_exists"].open = True
                    self.page.update()
                    return
                else:
                    client = req_user.get_client_by_telegram_name(telegram_name)

            dlg_user = ft.AlertDialog(
                modal=True,
                title=ft.Text("Добавить пользователя в администраторы?"),
                content=ft.Container(
                    height=170,
                    content=ft.Column(
                        controls=[
                            ft.TextField(label="Телефон", value=client.phone, height=40, read_only=True, text_size=15),
                            ft.TextField(label="Telegram", value=client.telegram_name, height=40, read_only=False,
                                         text_size=15),
                            ft.TextField(label="Имя", value=client.name, height=40, read_only=False, text_size=15),
                            ft.TextField(label="Email", value=client.email, height=40, read_only=False, text_size=15),
                        ]
                    )
                ),
                actions=[
                    ft.TextButton("Yes", on_click=lambda e: confirm_admin_handle_yes(dlg_user, client)),
                    ft.TextButton("No", on_click=lambda e: dialog_close(dlg_user)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
            )

            dlg_create.open = False
            self.page.open(dlg_user)
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
                ft.TextButton("No", on_click=lambda e: dialog_close(dlg_create)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

        self.page.open(dlg_create)
        self.page.update()