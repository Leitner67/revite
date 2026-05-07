import flet as ft
from core.constants import AppColors
from models.clientes import Cliente



def menu_principal_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Menu Principal"
    page.window_resizable = True
    page.bgcolor = AppColors.BACKGROUND
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    glow_shadow = ft.BoxShadow(
        spread_radius=0,
        blur_radius=16,
        color=AppColors.GLOW_PRIMARY,
        offset=ft.Offset(0, 0),
    )

    def hacer_reserva(e):
        from views.booking_view import booking_view
        booking_view(page, cliente)

    def ver_reservas(e):
        from views.reservas_view import ver_reservas_view
        ver_reservas_view(page, cliente)

    def ver_carros(e):
        from views.carros_view import ver_carros_view
        ver_carros_view(page, cliente)

    def perfil(e):
        from views.perfil_view import perfil_view
        perfil_view(page, cliente)

    def cerrar_sesion(e):
        from views.login_view import login_view
        login_view(page)

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, AppColors.BORDER),
        border_radius=10,
        bgcolor=AppColors.CARD,
        shadow=glow_shadow,
        content=ft.Text("Viajes Express", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
    )

    bienvenida = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Text(f"¡Qué más {cliente.get_nombres()}!", size=25, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
        ft.Text("¿Pa dónde vamos hoy?", size=16, color=AppColors.TEXT_SECONDARY),
        ft.Image(src=cliente.get_foto(), width=150, height=150, fit=ft.BoxFit.CONTAIN, border_radius=75),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    menu_opciones = ft.Column([
        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton(
            color=AppColors.BUTTON_PRIMARY_BG,
            content=ft.Text("Hacer Reserva", color=AppColors.BUTTON_TEXT, size=16),
            on_click=hacer_reserva,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=6),
        ),
        ft.ElevatedButton(
            color=AppColors.BUTTON_SECONDARY_BG,
            content=ft.Text("Mis Reservas", color=AppColors.BUTTON_TEXT, size=16),
            on_click=ver_reservas,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_HIGHLIGHT, elevation=6),
        ),
        ft.ElevatedButton(
            color=AppColors.BUTTON_NEUTRAL_BG,
            content=ft.Text("Carros Disponibles", color=AppColors.BUTTON_TEXT, size=16),
            on_click=ver_carros,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=5),
        ),
        ft.ElevatedButton(
            color=AppColors.BUTTON_SECONDARY_BG,
            content=ft.Text("Mi Perfil", color=AppColors.BUTTON_TEXT, size=16),
            on_click=perfil,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_HIGHLIGHT, elevation=6),
        ),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton(
            color=AppColors.BUTTON_DANGER_BG,
            content=ft.Text("Cerrar Sesión", color=AppColors.BUTTON_TEXT, size=14),
            on_click=cerrar_sesion,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_HIGHLIGHT, elevation=5),
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, bienvenida, menu_opciones)
    page.update()