import flet as ft

from pages.config.style import inputBgErrorColor

snack_message_pass = ft.SnackBar(
            content=ft.Text('Пароль изменен'),
            bgcolor=inputBgErrorColor
        )