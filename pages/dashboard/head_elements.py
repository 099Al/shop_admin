import flet as ft
from pages.style.style import *


def circle_avatar(role, **kwargs):
    if role == 'admin':
        return ft.CircleAvatar(
            content=ft.Text("A"),
            bgcolor=ft.colors.DEEP_ORANGE_200,
            **kwargs
        )
    elif role == 'super_admin':
        return ft.CircleAvatar(
            content=ft.Text("SA"),
            bgcolor=ft.colors.RED_500,
            **kwargs
        )
    else:
        return ft.CircleAvatar(
            content=ft.Text("U"),
            bgcolor=ft.colors.BLUE_500,
            **kwargs
        )

# start_header
def header(user_role):
    return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "Панель управления",
                        color=defaultFontColor,
                        size=20,
                        font_family="cupurum",
                    ),
                    ft.Container(
                        content=circle_avatar(user_role, foreground_image_src="/images/avatar.jpg"),
                        padding=ft.padding.only(right=30),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )