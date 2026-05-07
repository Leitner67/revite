import flet as ft
from core.constants import AppColors
from views.login_view import login_view, register_view

def main(page: ft.Page):
    page.title = "Revite"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = AppColors.BACKGROUND

    login_view(page)

ft.run(main)
