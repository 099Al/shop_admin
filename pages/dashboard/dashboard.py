import flet as ft
from flet_route import Params, Basket

from pages.dashboard.head_elements import circle_avatar, header
from pages.dashboard.menu_elements import logo, sidebar_menu
from pages.style.style import *
from dotenv import set_key, load_dotenv
from pathlib import Path
import os


class DashboardPage:
    load_dotenv()
    AUTH_USER = False
    check_token = ""  # не нужны т.к. данные берутся из сессии
    check_channel = ""
    env_file_path = Path("..") / ".env"
    token_bot = os.getenv("TOKEN_BOT")
    channel_link = os.getenv("CHANNEL")

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.AUTH_USER = page.session.get("auth_user")
        page.title = "Панель управления"
        page.window.width = defaultWidthWindow
        page.window.height = defaultWidthWindow
        page.window.min_width = 900
        page.window.min_height = 400
        page.fonts = {"cuprum": "fonts/Cuprum.ttf"}

        # self.user_role = page.session.get('auth_role')
        self.user_role = "admin"  # TEST
        # self.check_channel = page.session.get('CHANNEL')

        print(self.user_role)

        # def save_settings(e):
        # token = token_input.content.value
        # channel = channel_input.content.value
        # set_key(dotenv_path=self.env_file_path, key_to_set='TOKEN_BOT', value_to_set=token)
        # set_key(dotenv_path=self.env_file_path, key_to_set='CHANNEL', value_to_set=channel)
        # token_input.disabled = True  #после указания значений запретить изменение поля
        # channel_input.disabled = True
        # page.session.set('TOKEN', token) #сохранить значение в сессии
        # page.session.set('CHANNEL', channel) #сохранить значение в сессии
        # self.check_token = page.session.get('TOKEN')
        # self.check_channel = page.session.get('CHANNEL')



        def input_form(label, value):
            return ft.TextField(
                label=f"{label}",
                value=value,
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            )

        def input_disable(value):
            return ft.TextField(
                value=value,
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                disabled=True,
                color=secondaryFontColor,
            )

        return ft.View(
            "/dashboard",
            controls=[
                # ft.Container(content=input_form('введите токен бота'))
                ft.Row(
                    expand=True,
                    controls=[
                        # left
                        ft.Container(
                            expand=1,
                            content=ft.Column(controls=[logo, sidebar_menu]),
                            bgcolor=secondaryBgColor,
                        ),
                        # body center
                        ft.Container(
                            expand=4,
                            padding=ft.padding.symmetric(15, 10),
                            content=ft.Column([header(self.user_role)]),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
