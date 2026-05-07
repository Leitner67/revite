import flet as ft
from core.constants import AppColors
from data.database import cargar_reservas, eliminar_reserva


def ver_reservas_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Mis Reservas"
    page.window_resizable = True
    page.bgcolor = AppColors.BACKGROUND
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    glow_shadow = ft.BoxShadow(
        spread_radius=0,
        blur_radius=16,
        color=AppColors.GLOW_PRIMARY,
        offset=ft.Offset(0, 0),
    )

    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)

    reservas = cargar_reservas()
    mis_reservas = []
    for indice_global, r in enumerate(reservas):
        if r.get_cliente() and r.get_cliente().get_cedula() == cliente.get_cedula():
            mis_reservas.append((indice_global, r))

    def eliminar_reserva_click(indice_global):
        def handler(e):
            if eliminar_reserva(indice_global):
                page.overlay.append(
                    ft.SnackBar(
                        content=ft.Text("Reserva eliminada", color=AppColors.TEXT_PRIMARY),
                        bgcolor=AppColors.SUCCESS,
                    )
                )
                page.overlay[-1].open = True
                ver_reservas_view(page, cliente)
            else:
                page.overlay.append(
                    ft.SnackBar(
                        content=ft.Text("No se pudo eliminar la reserva", color=AppColors.TEXT_PRIMARY),
                        bgcolor=AppColors.ERROR,
                    )
                )
                page.overlay[-1].open = True
                page.update()

        return handler

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, AppColors.BORDER),
        border_radius=10,
        bgcolor=AppColors.CARD,
        shadow=glow_shadow,
        content=ft.Text("Mis Reservas", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
    )

    if not mis_reservas:
        contenido = ft.Column([
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            ft.Text("No tienes reservas todavía", size=20, color=AppColors.TEXT_SECONDARY),
            ft.Text("Dale en 'Hacer Reserva' para crear una", size=14, color=AppColors.TEXT_SECONDARY),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        reservas_widgets = []
        for i, (indice_global, reserva) in enumerate(mis_reservas):
            reserva_card = ft.Container(
                bgcolor=AppColors.CARD,
                padding=15,
                border_radius=10,
                width=400,
                shadow=glow_shadow,
                content=ft.Column([
                    ft.Text(f"Reserva #{i+1}", size=18, weight=ft.FontWeight.BOLD, color=AppColors.PRIMARY),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, color=AppColors.PRIMARY, size=20),
                        ft.Text(f"Origen: {reserva.get_origen()}", size=14, color=AppColors.TEXT_PRIMARY),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.FLAG, color=AppColors.HIGHLIGHT, size=20),
                        ft.Text(f"Destino: {reserva.get_destino()}", size=14, color=AppColors.TEXT_PRIMARY),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, color=AppColors.SECONDARY, size=20),
                        ft.Text(f"Horario: {reserva.get_horario()}", size=14, color=AppColors.TEXT_PRIMARY),
                    ]),
                    ft.Row([
                        ft.ElevatedButton(
                            color=AppColors.BUTTON_DANGER_BG,
                            content=ft.Text("Eliminar", color=AppColors.BUTTON_TEXT, size=13),
                            on_click=eliminar_reserva_click(indice_global),
                            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_HIGHLIGHT, elevation=5),
                        )
                    ], alignment=ft.MainAxisAlignment.END),
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
        ft.ElevatedButton(
            color=AppColors.BUTTON_NEUTRAL_BG,
            content=ft.Text("Volver al Menú", color=AppColors.BUTTON_TEXT, size=14),
            on_click=volver_menu,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=4),
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, contenido, botones)
    page.update()