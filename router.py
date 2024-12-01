import flet as ft
from flet_route import Routing, path

from pages.dashboard.dashboard import DashboardPage


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url='/', clear=True, view=DashboardPage().view),  #TEST
            #path(url='/dashboard', clear=True, view=DashboardPage().view),
            #path(url='/', clear=True, view=LoginPage().view),


        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes,
        )
        self.page.go(self.page.route) #переход на страницу
