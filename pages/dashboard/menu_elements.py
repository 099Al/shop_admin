import flet as ft

from pages.dashboard.content import Dash_Content
from pages.dashboard.types import EnumDashContent
from pages.style.style import *

# style_menu
style_menu = ft.ButtonStyle(
            color={
                ft.ControlState.HOVERED: ft.colors.WHITE,
                ft.ControlState.DEFAULT: menuFontColor,
            },
            overlay_color=hoverBgcolor,
            shadow_color=hoverBgcolor,
        )

# sidebar
logo = ft.Container(
            padding=ft.padding.symmetric(17, 13),
            content=ft.Row(
                controls=[
                    ft.Image(
                        src="/images/logo.jpg", width=45, height=32, fit=ft.ImageFit.FILL
                    ),
                    ft.Text(
                        "Candy",
                        expand=True,
                        color=defaultFontColor,
                        font_family="cuprum",
                        size=16,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

# menu
def sidebar_menu(content: Dash_Content):
    return ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=12, font_family="cuprum"),
                    ft.TextButton(
                        "Главная",
                        icon="space_dashboard_rounded",
                        style=style_menu,
                        on_click=lambda e: page.go("/dashboard"),
                    ),
                    ft.TextButton(
                        "Категории",
                        icon="post_add",
                        style=style_menu,
                        on_click=lambda e: content.update_content(EnumDashContent.CATEGORY),
                    ),
                    ft.TextButton(
                        "Товар"
                        , icon="verified_user"
                        , style=style_menu
                        , on_click=lambda e: content.update_content(EnumDashContent.PRODUCTS),
                    ),
                    ft.TextButton(
                        "Пользователи"
                        , icon="verified_user"
                        , style=style_menu
                        #, on_click=lambda e: update_content(),
                    ),
                    ft.TextButton(
                        "Клиенты"
                        , icon="verified_user"
                        , style=style_menu
                        , on_click=lambda e: page.go("/post"),
                    ),
                    ft.TextButton(
                        "Заказы"
                        , icon="verified_user"
                        , style=style_menu
                        , on_click=lambda e: page.go("/post"),
                    ),
                ]
            ),
        )