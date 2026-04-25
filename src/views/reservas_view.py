import flet as ft
from data.database import cargar_reservas


def ver_reservas_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Mis Reservas"
    page.window_resizable = True
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)

    reservas = cargar_reservas()
    mis_reservas = [r for r in reservas if r.get_cliente() and r.get_cliente().get_cedula() == cliente.get_cedula()]

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Mis Reservas", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
    )

    if not mis_reservas:
        contenido = ft.Column([
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            ft.Text("No tenés reservas todavía", size=20, color=ft.Colors.WHITE70),
            ft.Text("Dale en 'Hacer Reserva' pa crear una", size=14, color=ft.Colors.WHITE60),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        reservas_widgets = []
        for i, reserva in enumerate(mis_reservas):
            reserva_card = ft.Container(
                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                padding=15,
                border_radius=10,
                width=400,
                content=ft.Column([
                    ft.Text(f"Reserva #{i+1}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.GREEN, size=20),
                        ft.Text(f"Origen: {reserva.get_origen()}", size=14, color=ft.Colors.WHITE),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.FLAG, color=ft.Colors.RED, size=20),
                        ft.Text(f"Destino: {reserva.get_destino()}", size=14, color=ft.Colors.WHITE),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.ORANGE, size=20),
                        ft.Text(f"Horario: {reserva.get_horario()}", size=14, color=ft.Colors.WHITE),
                    ]),
                ])
            )
            reservas_widgets.append(reserva_card)
            reservas_widgets.append(ft.Divider(height=15, color=ft.Colors.TRANSPARENT))

        contenido = ft.Column(
            reservas_widgets,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )

    botones = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Button(
            color=ft.Colors.GREY, 
            content=ft.Text("Volver al Menú", color=ft.Colors.WHITE, size=14), 
            on_click=volver_menu,
            width=250
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, contenido, botones)
    page.update()