import flet as ft
from core.constants import AppColors
from models.clientes import Cliente
from data.database import guardar_cliente, cargar_clientes, buscar_cliente_por_cedula
from views.home_view import menu_principal_view

foto_cliente = ft.Image(src="assets/default.png", width=100, height=100, fit=ft.BoxFit.COVER)

def login_view(page: ft.Page):
    page.controls.clear()
    page.title = "Iniciar sesion"
    page.window_resizable = True
    page.bgcolor = AppColors.BACKGROUND
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    glow_shadow = ft.BoxShadow(
        spread_radius=0,
        blur_radius=18,
        color=AppColors.GLOW_PRIMARY,
        offset=ft.Offset(0, 0),
    )

    cedula_sesion = ft.TextField(label="Cedula", width=220, color=AppColors.TEXT_PRIMARY, bgcolor=AppColors.CARD, border_color=AppColors.BORDER, focused_border_color=AppColors.PRIMARY)
    contraseña = ft.TextField(label="Contraseña", width=220, password=True, color=AppColors.TEXT_PRIMARY, bgcolor=AppColors.CARD, border_color=AppColors.BORDER, focused_border_color=AppColors.PRIMARY)
    status_message = ft.Text("", size=14, color=AppColors.ERROR)

    def sesion_iniciada(e):
        cliente = buscar_cliente_por_cedula(cedula_sesion.value)
        
        if cliente and cliente.get_contraseña() == contraseña.value:
            menu_principal_view(page, cliente)
        else:
            status_message.value = "Cédula o contraseña incorrecta"
            page.update()

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, AppColors.BORDER),
        border_radius=10,
        bgcolor=AppColors.CARD,
        shadow=glow_shadow,
        content=ft.Text("Cliente", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
    )

    info_sesion = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Text("Iniciar sesion", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
        cedula_sesion,
        contraseña,
        ft.ElevatedButton(
            "Login",
            bgcolor=AppColors.BUTTON_PRIMARY_BG,
            color=AppColors.BUTTON_TEXT,
            on_click=sesion_iniciada,
            width=220,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=6),
        ),
        status_message,
        ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    registrarse = ft.Column([
        ft.Text("¿No tienes una cuenta? Registrate", size=12, color=AppColors.TEXT_SECONDARY),
        ft.ElevatedButton(
            "Registrarse",
            bgcolor=AppColors.BUTTON_SECONDARY_BG,
            color=AppColors.BUTTON_TEXT,
            on_click=lambda _: register_view(page),
            width=220,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_HIGHLIGHT, elevation=6),
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, info_sesion, registrarse)
    page.update()

def register_view(page: ft.Page):
    page.controls.clear()
    page.title = "Registro"
    page.window_resizable = True
    page.bgcolor = AppColors.BACKGROUND
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    glow_shadow = ft.BoxShadow(
        spread_radius=0,
        blur_radius=18,
        color=AppColors.GLOW_PRIMARY,
        offset=ft.Offset(0, 0),
    )

    cedula_field = ft.TextField(label="Cédula", width=220, color=AppColors.TEXT_PRIMARY, bgcolor=AppColors.CARD, border_color=AppColors.BORDER, focused_border_color=AppColors.PRIMARY)
    nombres_field = ft.TextField(label="Nombres", width=220, color=AppColors.TEXT_PRIMARY, bgcolor=AppColors.CARD, border_color=AppColors.BORDER, focused_border_color=AppColors.PRIMARY)
    apellidos_field = ft.TextField(label="Apellidos", width=220, color=AppColors.TEXT_PRIMARY, bgcolor=AppColors.CARD, border_color=AppColors.BORDER, focused_border_color=AppColors.PRIMARY)
    celular_field = ft.TextField(label="Celular", width=220, color=AppColors.TEXT_PRIMARY, bgcolor=AppColors.CARD, border_color=AppColors.BORDER, focused_border_color=AppColors.PRIMARY)
    contraseña_field = ft.TextField(label="Contraseña", width=220, password=True, color=AppColors.TEXT_PRIMARY, bgcolor=AppColors.CARD, border_color=AppColors.BORDER, focused_border_color=AppColors.PRIMARY)
    async def seleccionar_archivo(e):
        picker = ft.FilePicker()
        file = await picker.pick_files(allow_multiple=False)
        if file:
            foto_field.value = file[0].path
            page.update()
    foto_field = ft.ElevatedButton(text="Seleccionar foto", icon=ft.Icons.PHOTO, width=200, on_click=seleccionar_archivo)

    mensaje_estado = ft.Text("", size=14, color=AppColors.SUCCESS)

    def registrar_click(e):
        if not cedula_field.value or not nombres_field.value or not apellidos_field.value or not celular_field.value:
            mensaje_estado.value = "Por favor complete todos los campos obligatorios"
            mensaje_estado.color = AppColors.ERROR
            page.update()
            return

        try:
            cliente = Cliente(
                cedula=cedula_field.value,
                nombres=nombres_field.value,
                apellidos=apellidos_field.value,
                contraseña=contraseña_field.value,
                celular=celular_field.value,
                foto=foto_field.value
            )

            guardar_cliente(cliente)
            mensaje_estado.value = "Cliente registrado exitosamente!"
            mensaje_estado.color = AppColors.SUCCESS
            cedula_field.value = ""
            nombres_field.value = ""
            apellidos_field.value = ""
            celular_field.value = ""
            contraseña_field.value = ""
            foto_field.value = None

        except Exception as ex:
            mensaje_estado.value = f"Error: {str(ex)}"
            mensaje_estado.color = AppColors.ERROR

        page.update()

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, AppColors.BORDER),
        border_radius=10,
        bgcolor=AppColors.CARD,
        shadow=glow_shadow,
        content=ft.Text("Cliente", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
    )

    register = ft.Column(
        [
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Text("Registrar", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            cedula_field,
            nombres_field,
            apellidos_field,
            celular_field,
            contraseña_field,
            foto_field,
            ft.ElevatedButton(
                "Registrar",
                bgcolor=AppColors.BUTTON_PRIMARY_BG,
                color=AppColors.BUTTON_TEXT,
                on_click=registrar_click,
                width=220,
                style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=6),
            ),
            mensaje_estado,
            ft.ElevatedButton(
                "Volver",
                bgcolor=AppColors.BUTTON_NEUTRAL_BG,
                color=AppColors.BUTTON_TEXT,
                on_click=lambda _: login_view(page),
                width=220,
                style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=4),
            ),
        ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, register)
    page.update()
