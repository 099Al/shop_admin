import flet as ft
from flet_route import Params, Basket

from database.connect import DataBase
from database.models.models import Admin
from database.requests.req_login import ReqAdmins
from pages.login.login_elements import email_input, password_input, error_message
from utils.functions import hash_password_
from pages.style.style import *


class LoginPage:
    def __init__(self):
        self.email_input = email_input
        self.password_input = password_input
        self.error_message = error_message

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = "Страница авторизации"
        page.window.width = defaultWidthWindow
        page.window.height = defaultWidthWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"cuprum": "fonts/Cuprum.ttf"}

        def authorization(e):
            db = DataBase()
            req = ReqAdmins(db)
            email = self.email_input.content.value
            password = self.password_input.content.value
            hash_password = hash_password_(password)
            login_resp: Admin = req.authorization(email, hash_password)
            if login_resp:
                page.session.set('auth_user', True)
                page.session.set('auth_role', login_resp.role)
                page.go('/dashboard')
            else:
                self.error_message.open = True  # error_message определен выше
                self.error_message.update()  #Вывод на экран

        return ft.View(
            "/",
            controls=[
                # ft.Text('Login'),           #элемент с текстов
                # ft.ElevatedButton('Страница регистрации', on_click=lambda e: page.go('/signup')) #кнопка для перехода
                # self.email_input
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=2,  # размер контейнера
                            padding=ft.padding.all(40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "Вход в систему",
                                        color=defaultFontColor,
                                        size=25,
                                        weight=ft.FontWeight.NORMAL,
                                    ),
                                    self.error_message, #объект для оповещений
                                    self.email_input,
                                    self.password_input,
                                    ft.Container(
                                        ft.Text("Авторизация", color=defaultFontColor),
                                        alignment=ft.alignment.center,
                                        height=40,
                                        bgcolor=hoverBgcolor,
                                        on_click=lambda e: authorization(e)
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=3,
                            image=ft.DecorationImage(
                                src="/images/bg_login.jpg",
                                fit=ft.ImageFit.COVER,
                            ),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        name=ft.icons.LOCK_PERSON_ROUNDED,
                                        color=hoverBgcolor,
                                        size=140,
                                    ),
                                    ft.Text(
                                        "Авторизация",
                                        color=hoverBgcolor,
                                        size=15,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )
