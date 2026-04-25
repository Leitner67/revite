import flet as ft
from models.clientes import Cliente
from data.database import guardar_cliente, cargar_clientes, buscar_cliente_por_cedula
from views.home_view import menu_principal_view

foto_cliente = ft.Image(src="assets/default.png", width=100, height=100, fit=ft.BoxFit.COVER)

def login_view(page: ft.Page):
    page.controls.clear()
    page.title = "Iniciar sesion"
    page.window_resizable = True
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    cedula_sesion = ft.TextField(label="Cedula", width=200, color=ft.Colors.WHITE, bgcolor=ft.Colors.SURFACE)
    contraseña = ft.TextField(label="Contraseña", width=200, password=True, color=ft.Colors.WHITE, bgcolor=ft.Colors.SURFACE)
    status_message = ft.Text("", size=14, color=ft.Colors.RED)

    def sesion_iniciada(e):
        cliente = buscar_cliente_por_cedula(cedula_sesion.value)
        
        if cliente and cliente.get_contraseña() == contraseña.value:
            menu_principal_view(page, cliente)
        else:
            status_message.value = "Cédula o contraseña incorrecta"
            page.update()

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Cliente", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
    )

    info_sesion = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Text("Iniciar sesion", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        cedula_sesion,
        contraseña,
        ft.Button(color=ft.Colors.BLUE, content=ft.Text("Login", color=ft.Colors.WHITE), on_click=sesion_iniciada),
        status_message,
        ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    registrarse = ft.Column([
        ft.Text("¿No tienes una cuenta? Registrate", size=12, color=ft.Colors.WHITE),
        ft.Button(color=ft.Colors.BLUE, content=ft.Text("Registrarse", color=ft.Colors.WHITE), on_click=lambda _: register_view(page)),
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
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    cedula_field = ft.TextField(label="Cédula", width=200, color=ft.Colors.WHITE, bgcolor=ft.Colors.SURFACE)
    nombres_field = ft.TextField(label="Nombres", width=200, color=ft.Colors.WHITE, bgcolor=ft.Colors.SURFACE)
    apellidos_field = ft.TextField(label="Apellidos", width=200, color=ft.Colors.WHITE, bgcolor=ft.Colors.SURFACE)
    celular_field = ft.TextField(label="Celular", width=200, color=ft.Colors.WHITE, bgcolor=ft.Colors.SURFACE)
    contraseña_field = ft.TextField(label="Contraseña", width=200, password=True, color=ft.Colors.WHITE, bgcolor=ft.Colors.SURFACE)
    silla_de_ruedas_field = ft.Checkbox(label="Usa silla de ruedas", value=False, on_change=True) 
    async def seleccionar_archivo(e):
        picker = ft.FilePicker()
        file = await picker.pick_files(allow_multiple=False)
        if file:
            foto_field.value = file[0].path
            page.update()
    foto_field = ft.Button(content=ft.Text("Seleccionar foto"), width=200, on_click=seleccionar_archivo)

    mensaje_estado = ft.Text("", size=14, color=ft.Colors.GREEN)

    def registrar_click(e):
        if not cedula_field.value or not nombres_field.value or not apellidos_field.value or not celular_field.value:
            mensaje_estado.value = "Por favor complete todos los campos obligatorios"
            mensaje_estado.color = ft.Colors.RED
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

            if guardar_cliente(cliente):
                mensaje_estado.value = "Cliente registrado exitosamente!"
                mensaje_estado.color = ft.Colors.GREEN
                cedula_field.value = ""
                nombres_field.value = ""
                apellidos_field.value = ""
                celular_field.value = ""
                contraseña_field.value = ""
                foto_field.value = None
            else:
                mensaje_estado.value = "Error al guardar el cliente"
                mensaje_estado.color = ft.Colors.RED

        except Exception as ex:
            mensaje_estado.value = f"Error: {str(ex)}"
            mensaje_estado.color = ft.Colors.RED

        page.update()

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Cliente", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
    )

    register = ft.Column(
        [
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Text("Registrar", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            cedula_field,
            nombres_field,
            apellidos_field,
            celular_field,
            contraseña_field,
            foto_field,
            silla_de_ruedas_field,
            ft.Button(color=ft.Colors.BLUE, content=ft.Text("Registrar", color=ft.Colors.WHITE), on_click=registrar_click),
            mensaje_estado,
            ft.Button(color=ft.Colors.GREY, content=ft.Text("Volver", color=ft.Colors.WHITE), on_click=lambda _: login_view(page)),
        ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, register)
    page.update()
