import flet as ft
from core.constants import AppColors
from models.reservas import Reserva
from data.database import cargar_carros, guardar_reserva


def booking_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Booking"
    page.window_resizable = True
    page.bgcolor = AppColors.BACKGROUND
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START

    glow_shadow = ft.BoxShadow(
        spread_radius=0,
        blur_radius=16,
        color=AppColors.GLOW_PRIMARY,
        offset=ft.Offset(0, 0),
    )

    horario_seleccionado = None
    carro_seleccionado = None
    carros_disponibles = cargar_carros()
    ciudades_disponibles = sorted(set([
        "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Cúcuta", "Pereira",
        "Manizales", "Armenia", "Ibagué", "Neiva", "Villavicencio", "Pasto", "Popayán", "Santa Marta",
        "Sincelejo", "Valledupar", "Montería", "Tunja", "Florencia", "Quibdó", "Riohacha", "Yopal",
        "Leticia", "San Andrés", "Apartadó", "Turbo", "Soacha", "Palmira", "Buenaventura", "Tuluá",
        "Girardot", "Facatativá", "Zipaquirá", "Chía", "Mosquera", "Fusagasugá", "Sogamoso", "Duitama",
        "Ipiales", "Tumaco", "Maicao", "Ciénaga", "Magangué", "Lorica", "Ocaña", "Pamplona", "Aguachica",
        "La Dorada", "Honda", "Espinal", "Garzón", "Pitalito", "Carepa", "Necoclí", "Rionegro", "Envigado",
        "Itagüí", "Bello", "Copacabana", "Girón", "Floridablanca", "Barrancabermeja", "Malambo", "Soledad",
        "Sabanalarga", "El Banco", "Plato", "Fundación", "San Gil", "Barbosa", "Socorro", "Chiquinquirá",
        "Guaduas", "Villeta", "La Vega", "Anapoima", "Melgar", "Salento", "Filandia", "Circasia", "Montenegro",
        "La Tebaida", "Jamundí", "Yumbo", "Pradera", "Florida", "Cartago", "Zarzal", "Buga", "Guacarí",
        "Ginebra", "Andalucía", "Sevilla", "Caicedonia", "La Unión", "Roldanillo", "Toro", "Versalles",
        "El Cerrito", "Candelaria", "Dagua", "Calima", "Restrepo", "Trujillo", "Riofrío", "Bolívar", "El Dovio",
        "Argelia", "Alcalá", "Ulloa", "Obando", "La Victoria", "San Pedro", "Bugalagrande", "Guadalajara de Buga",
        "Tocancipá", "Cajicá", "Sibaté", "La Calera", "Guasca", "Sesquilé", "Nemocón", "Tabio", "Tenjo",
        "Subachoque", "El Rosal", "Madrid", "Funza", "Cota", "Zipacón", "Anolaima", "La Mesa", "Tena", "Viotá",
        "San Antonio del Tequendama", "Apulo", "Jerusalén", "Nilo", "Ricaurte", "Agua de Dios", "Tocaima"
    ]), key=lambda ciudad: ciudad.lower())

    periodo_group = ft.RadioGroup(
        value="AM",
        content=ft.Row(
            [
                ft.Radio(value="AM", label="AM"),
                ft.Radio(value="PM", label="PM"),
            ],
            spacing=20,
        ),
    )

    hora_field = ft.Dropdown(
        label="Hora",
        hint_text="1 a 12",
        options=[ft.dropdown.Option(str(hora)) for hora in range(1, 13)],
        width=120,
        color=AppColors.TEXT_PRIMARY,
        bgcolor=AppColors.CARD,
    )

    minuto_field = ft.Dropdown(
        label="Minutos",
        hint_text="00, 15, 30, 45",
        options=[ft.dropdown.Option(minuto) for minuto in ["00", "15", "30", "45"]],
        width=120,
        color=AppColors.TEXT_PRIMARY,
        bgcolor=AppColors.CARD,
    )

    origen_field = ft.Dropdown(
        label="Origen",
        hint_text="Selecciona ciudad",
        options=[ft.dropdown.Option(ciudad) for ciudad in ciudades_disponibles],
        width=300,
        color=AppColors.TEXT_PRIMARY,
        bgcolor=AppColors.CARD,
        enable_search=True,
        enable_filter=True,
    )

    destino_field = ft.Dropdown(
        label="Destino",
        hint_text="Selecciona ciudad",
        options=[ft.dropdown.Option(ciudad) for ciudad in ciudades_disponibles],
        width=300,
        color=AppColors.TEXT_PRIMARY,
        bgcolor=AppColors.CARD,
        enable_search=True,
        enable_filter=True,
    )

    mensaje_estado = ft.Text("", size=14, color=AppColors.SUCCESS)

    def carro_click(carro, container):
        def handler(e):
            nonlocal carro_seleccionado
            carro_seleccionado = carro
            
            for c in carros_containers:
                c.border = ft.Border.all(2, ft.Colors.TRANSPARENT)
            
            container.border = ft.Border.all(2, AppColors.PRIMARY)
            page.update()
        
        return handler

    def confirmar_reserva(e):
        nonlocal horario_seleccionado
        origen_ingresado = (origen_field.value or "").strip()
        destino_ingresado = (destino_field.value or "").strip()
        hora_ingresada = (hora_field.value or "").strip()
        minuto_ingresado = (minuto_field.value or "").strip()
        periodo_ingresado = (periodo_group.value or "AM").strip()
        if hora_ingresada and minuto_ingresado:
            horario_seleccionado = f"{hora_ingresada}:{minuto_ingresado} {periodo_ingresado}"
        else:
            horario_seleccionado = None

        if not horario_seleccionado:
            mensaje_estado.value = "Selecciona un horario"
            mensaje_estado.color = AppColors.ERROR
            page.update()
            return

        if not origen_ingresado:
            mensaje_estado.value = "Selecciona el origen"
            mensaje_estado.color = AppColors.ERROR
            page.update()
            return

        if not destino_ingresado:
            mensaje_estado.value = "Selecciona el destino"
            mensaje_estado.color = AppColors.ERROR
            page.update()
            return

        if origen_ingresado == destino_ingresado:
            mensaje_estado.value = "Origen y destino no pueden ser iguales"
            mensaje_estado.color = AppColors.ERROR
            page.update()
            return

        if not carro_seleccionado:
            mensaje_estado.value = "Selecciona un carro"
            mensaje_estado.color = AppColors.ERROR
            page.update()
            return

        reserva = Reserva(
            origen=origen_ingresado,
            destino=destino_ingresado,
            horario=horario_seleccionado,
            cliente=cliente
        )

        if guardar_reserva(reserva):
            mensaje_estado.value = "¡Reserva confirmada!"
            mensaje_estado.color = AppColors.SUCCESS
            hora_field.value = None
            minuto_field.value = None
            periodo_group.value = "AM"
            origen_field.value = None
            destino_field.value = None
            page.update()
        else:
            mensaje_estado.value = "Error al guardar la reserva"
            mensaje_estado.color = AppColors.ERROR
            page.update()

    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)

    horarios_container = ft.Container(
        bgcolor=AppColors.CARD,
        padding=15,
        border_radius=10,
        shadow=glow_shadow,
        content=ft.Column([
            ft.Text("Horarios", size=18, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            ft.Row([hora_field, minuto_field], spacing=10),
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            ft.Text("Periodo", size=14, color=AppColors.TEXT_SECONDARY),
            periodo_group,
        ])
    )

    destino_container = ft.Container(
        bgcolor=AppColors.CARD,
        padding=15,
        border_radius=10,
        width=350,
        shadow=glow_shadow,
        content=ft.Column([
            ft.Text("Ruta", size=18, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            origen_field,
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
            border=ft.Border.all(2, AppColors.BORDER),
            alignment=ft.Alignment.CENTER,
            content=ft.Text("X", size=20, color=AppColors.TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        )
        
        carro_container = ft.Container(
            bgcolor=AppColors.CARD,
            padding=10,
            border_radius=10,
            width=100,
            border=ft.Border.all(2, ft.Colors.TRANSPARENT),
            content=ft.Column([
                caja,
                ft.Text(carro.get_placa(), size=14, color=AppColors.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
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
        ft.Text("Carros Disponibles", size=18, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
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
        border=ft.Border.all(1, AppColors.BORDER),
        border_radius=10,
        bgcolor=AppColors.CARD,
        shadow=glow_shadow,
        content=ft.Text("Booking", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
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
        ft.ElevatedButton(
            color=AppColors.BUTTON_PRIMARY_BG,
            content=ft.Text("Confirmar Reserva", color=AppColors.BUTTON_TEXT, size=16),
            on_click=confirmar_reserva,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=6),
        ),
        mensaje_estado,
        ft.ElevatedButton(
            color=AppColors.BUTTON_NEUTRAL_BG,
            content=ft.Text("Volver", color=AppColors.BUTTON_TEXT, size=14),
            on_click=volver_menu,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=4),
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, ft.Divider(height=20, color=ft.Colors.TRANSPARENT), contenido, botones)
    page.update()