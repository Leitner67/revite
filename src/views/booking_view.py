import flet as ft
from models.reservas import Reserva
from data.database import cargar_carros, guardar_reserva


def booking_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Booking"
    page.window_resizable = True
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START

    horario_seleccionado = None
    carro_seleccionado = None
    carros_disponibles = cargar_carros()

    destino_field = ft.TextField(
        label="Destino",
        multiline=True,
        min_lines=5,
        max_lines=10,
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
    )

    mensaje_estado = ft.Text("", size=14, color=ft.Colors.GREEN)

    def horario_click(horario):
        def handler(e):
            nonlocal horario_seleccionado
            horario_seleccionado = horario
            
            for checkbox in horarios_checkboxes:
                checkbox.value = False
            
            e.control.value = True
            page.update()
        
        return handler

    def carro_click(carro, container):
        def handler(e):
            nonlocal carro_seleccionado
            carro_seleccionado = carro
            
            for c in carros_containers:
                c.border = ft.Border.all(2, ft.Colors.TRANSPARENT)
            
            container.border = ft.Border.all(2, ft.Colors.BLUE)
            page.update()
        
        return handler

    def confirmar_reserva(e):
        if not horario_seleccionado:
            mensaje_estado.value = "Selecciona un horario"
            mensaje_estado.color = ft.Colors.RED
            page.update()
            return

        if not destino_field.value:
            mensaje_estado.value = "Escribe el destino"
            mensaje_estado.color = ft.Colors.RED
            page.update()
            return

        if not carro_seleccionado:
            mensaje_estado.value = "Selecciona un carro"
            mensaje_estado.color = ft.Colors.RED
            page.update()
            return

        reserva = Reserva(
            origen="Espinal",
            destino=destino_field.value,
            horario=horario_seleccionado,
            cliente=cliente
        )

        if guardar_reserva(reserva):
            mensaje_estado.value = "¡Reserva confirmada!"
            mensaje_estado.color = ft.Colors.GREEN
            destino_field.value = ""
            page.update()
        else:
            mensaje_estado.value = "Error al guardar la reserva"
            mensaje_estado.color = ft.Colors.RED
            page.update()

    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)

    horarios_checkboxes = []
    horarios = ["6:00", "6:30", "7:00", "9:30"]
    
    horarios_widgets = []
    for horario in horarios:
        checkbox = ft.Checkbox(value=False, on_change=horario_click(horario))
        horarios_checkboxes.append(checkbox)
        horarios_widgets.append(
            ft.Row([
                checkbox,
                ft.Text(horario, size=16, color=ft.Colors.WHITE),
            ])
        )

    horarios_container = ft.Container(
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        padding=15,
        border_radius=10,
        content=ft.Column([
            ft.Text("Horarios", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            *horarios_widgets,
        ])
    )

    destino_container = ft.Container(
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        padding=15,
        border_radius=10,
        width=350,
        content=ft.Column([
            ft.Text("Destino", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            destino_field,
        ])
    )

    carros_containers = []
    carros_widgets = []
    
    for carro in carros_disponibles[:4]:
        caja = ft.Container(
            width=60,
            height=60,
            border=ft.Border.all(2, ft.Colors.WHITE),
            alignment=ft.Alignment. CENTER,
            content=ft.Text("X", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        )
        
        carro_container = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            padding=10,
            border_radius=10,
            width=100,
            border=ft.Border.all(2, ft.Colors.TRANSPARENT),
            content=ft.Column([
                caja,
                ft.Text(carro.get_placa(), size=14, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=carro_click(carro, None)
        )
        
        carro_container.on_click = carro_click(carro, carro_container)
        carros_containers.append(carro_container)
        carros_widgets.append(carro_container)

    carros_grid = ft.Column([
        ft.Text("Carros Disponibles", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Row([
            carros_widgets[0] if len(carros_widgets) > 0 else ft.Container(),
            carros_widgets[1] if len(carros_widgets) > 1 else ft.Container(),
        ]),
        ft.Row([
            carros_widgets[2] if len(carros_widgets) > 2 else ft.Container(),
            carros_widgets[3] if len(carros_widgets) > 3 else ft.Container(),
        ]),
    ])

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Booking", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
    )

    contenido = ft.Row([
        horarios_container,
        destino_container,
        carros_grid,
    ],
    alignment=ft.MainAxisAlignment.START,
    )

    botones = ft.Column([
        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
        ft.Button(
            color=ft.Colors.GREEN, 
            content=ft.Text("Confirmar Reserva", color=ft.Colors.WHITE, size=16), 
            on_click=confirmar_reserva,
            width=250
        ),
        mensaje_estado,
        ft.Button(
            color=ft.Colors.GREY, 
            content=ft.Text("Volver", color=ft.Colors.WHITE, size=14), 
            on_click=volver_menu,
            width=250
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, ft.Divider(height=20, color=ft.Colors.TRANSPARENT), contenido, botones)
    page.update()