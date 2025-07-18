import flet as ft

from pages.dashboard.content_choose import Dash_Content
from pages.dashboard.types import EnumDashContent
from pages.config.style import *

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
def sidebar_menu(content_template: Dash_Content):
    return ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text("МЕНЮ", color=menuFontColor, size=12, font_family="cuprum"),
                    ft.TextButton(
                        "Категории",
                        icon=ft.icons.CATEGORY,
                        style=style_menu,
                        on_click=lambda e: content_template.update_content(EnumDashContent.CATEGORY),
                    ),
                    ft.TextButton(
                        "Товар"
                        , icon="post_add"
                        , style=style_menu
                        , on_click=lambda e: content_template.update_content(EnumDashContent.PRODUCTS),
                    ),
                    ft.TextButton(
                        "Товар и Категории"
                        , icon=ft.Icons.FEATURED_PLAY_LIST_OUTLINED
                        , style=style_menu
                        , on_click=lambda e: content_template.update_content(EnumDashContent.PRODUCTS_AND_CATEGORIES),
                    ),
                    ft.TextButton(
                        "Пользователи"
                        , icon=ft.icons.ADMIN_PANEL_SETTINGS
                        , style=style_menu
                        , on_click=lambda e: content_template.update_content(EnumDashContent.ADMINS),
                    ),
                    ft.TextButton(
                        "Клиенты"
                        , icon=ft.icons.SUPERVISED_USER_CIRCLE
                        , style=style_menu
                        , on_click=lambda e: content_template.update_content(EnumDashContent.CLIENTS),
                    ),
                    ft.TextButton(
                        "Заказы"
                        , icon=ft.icons.SHOPPING_BASKET
                        , style=style_menu
                        , on_click=lambda e: content_template.update_content(EnumDashContent.ORDERS),
                    ),
                ]
            ),
        )