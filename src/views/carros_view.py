import flet as ft
from data.database import cargar_carros


def ver_carros_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Carros Disponibles"
    page.window_resizable = True
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)

    carros = cargar_carros()

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Carros Disponibles", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
    )

    if not carros:
        contenido = ft.Column([
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            ft.Text("No hay carros disponibles", size=20, color=ft.Colors.WHITE70),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        carros_widgets = []
        for carro in carros:
            carro_card = ft.Container(
                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                padding=15,
                border_radius=10,
                width=350,
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.DIRECTIONS_CAR, color=ft.Colors.BLUE, size=30),
                        ft.Text(f"{carro.get_marca()} {carro.get_modelo()}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ]),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    ft.Row([
                        ft.Text("Año:", size=14, color=ft.Colors.WHITE70),
                        ft.Text(str(carro.get_ano()), size=14, color=ft.Colors.WHITE),
                    ]),
                    ft.Row([
                        ft.Text("Placa:", size=14, color=ft.Colors.WHITE70),
                        ft.Text(carro.get_placa(), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                    ]),
                ])
            )
            carros_widgets.append(carro_card)
            carros_widgets.append(ft.Divider(height=15, color=ft.Colors.TRANSPARENT))

        contenido = ft.Column(
            carros_widgets,
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