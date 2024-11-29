import flet as ft
from utils.style import *

email_input = ft.Container(
        content=ft.TextField(
            label="Укажите Email",
            bgcolor=secondaryBgColor,
            border=ft.InputBorder.NONE,
            filled=True,
            color=secondaryFontColor,
        ),
        border_radius=15,
    )


password_input = ft.Container(
    content=ft.TextField(
        label="Введите пароль",
        password=True,
        can_reveal_password=True,
        bgcolor=secondaryBgColor,
        border=ft.InputBorder.NONE,
        filled=True,
        color=secondaryFontColor,
    ),
    border_radius=15,
)

error_message = ft.SnackBar(
    content=ft.Text('Ошибка авторизации'),
    bgcolor=inputBgErrorColor
)