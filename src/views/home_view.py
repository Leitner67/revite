import flet as ft
from models.clientes import Cliente



def menu_principal_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Menu Principal"
    page.window_resizable = True
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

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
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Viajes Express", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
    )

    bienvenida = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Text(f"¡Qué más {cliente.get_nombres()}!", size=25, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        ft.Text("¿Pa dónde vamos hoy?", size=16, color=ft.Colors.WHITE70),
        ft.Image(src=cliente.get_foto(), width=150, height=150, fit=ft.BoxFit.CONTAIN, border_radius=75),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    menu_opciones = ft.Column([
        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
        ft.Button(
            color=ft.Colors.BLUE, 
            content=ft.Text("Hacer Reserva", color=ft.Colors.WHITE, size=16), 
            on_click=hacer_reserva,
            width=250
        ),
        ft.Button(
            color=ft.Colors.GREEN, 
            content=ft.Text("Mis Reservas", color=ft.Colors.WHITE, size=16), 
            on_click=ver_reservas,
            width=250
        ),
        ft.Button(
            color=ft.Colors.ORANGE, 
            content=ft.Text("Carros Disponibles", color=ft.Colors.WHITE, size=16), 
            on_click=ver_carros,
            width=250
        ),
        ft.Button(
            color=ft.Colors.PURPLE, 
            content=ft.Text("Mi Perfil", color=ft.Colors.WHITE, size=16), 
            on_click=perfil,
            width=250
        ),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Button(
            color=ft.Colors.RED_700, 
            content=ft.Text("Cerrar Sesión", color=ft.Colors.WHITE, size=14), 
            on_click=cerrar_sesion,
            width=250
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, bienvenida, menu_opciones)
    page.update()