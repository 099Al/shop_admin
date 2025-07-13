import flet as ft

from pages.dashboard.dashboard import DashboardPage
from pages.login.login import LoginPage


d_routes = {
    "/": DashboardPage(),
    "/dashboard": DashboardPage(),
    #"/": LoginPage(),
}


def main(page: ft.Page):

    def route_change(route):
        page.views.clear()
        curr_view = d_routes[page.route]
        page.views.append(curr_view.view(page, None, None))

        page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                #track_visibility=True,
                track_border_color=ft.Colors.BLUE,
                #thumb_visibility=True,
                thumb_color={
                    ft.ControlState.HOVERED: ft.Colors.GREY_300,
                    ft.ControlState.DEFAULT: ft.Colors.GREY_800,
                },
                #thickness=30,
                #radius=15,
                #main_axis_margin=5,
                #cross_axis_margin=10,
            )
        )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    #page.on_view_pop = view_pop
    page.go(page.route)



if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')


    #test/123